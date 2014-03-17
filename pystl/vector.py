# -*- coding: utf-8 -*-
"""
vector
~~~~~~

C++ STL vector wrapper implementing Python list interface.

It defines an adapter on top of a newly created or existent `std::vector`
instance.

It can be used with either an already existing on-memory STL vector through a
void pointer or by creating a new vector which can be later passed to C code.

Managed new object
-------------------

It can be used like a normal list, by creating the object and using it. It
will free its memory when the object is no longer referenced.

.. code::
    >>> vector = VectorInt()
    >>> list(vector)
    []
    >> del vector  # will call delete

Unmanaged new object
--------------------

vector deletion at garbage collection time can be avoided by setting the
managed flag to False:

.. code::
    >> vector = VectorInt(managed=False)
    >> vector.extend(complex_business_logic())
    >> from ctypes import c_void_p
    >> c_void_p(vector.vector)
    c_void_p(34212576)

This won't be freed and the reference can be further used and returned back to
C and manage it from there by casting it back to it's right type and manually
calling `delete` on the pointer.

Already existing object
------------------------

But it will also accept a pointer to an existing vector, and will not touch it
and free it at object garbage collection time.

.. code::
    >> pointer = ...  # void pointer to vector<int>
    >> vector = VectorInt(ref=pointer)
    >> list(vector)
    >> [1, 2, 3]
    >> del vector  # will NOT call C++ delete

This is useful to handle *c-resident* memory with which we just want to read
and modify without copying nor freeing.

Copy into a python object
--------------------------

All the data can be easily copied into any python collection by iterating over
the object.

.. code::
    >>> set(vector)
    set(1, 2, 3)
    >>> map(zip(vector, vector))
    {1:1, 2:2, 3:3}

Types
-----

Notice that this classes must be type consistent and do not manage all
possible types.

A new wrapper must be set per each new type, linked to C wrapper
functions, which will call C++ code and instantiate all the needed templates
at compile time which deal with the desired new type.

This is annoying, so effort has been put into making it as decoupled as possible.

The :class:`Vector` class defines most of `list` logic and methods, using
`vector_*` functions, which implement all the operations by a given container
and type, exposing it through a pure C interface wrapper. They have to be
referenced in Python by subclassing the `Vector` class and setting references
to the needed functions.

.. code::
    class VectorInt(Vector):
        vector_new = lib.py_vector_int_new
        vector_new.restype = c_void_p
        vector_new.argtypes = []
        (..)

Wich is using a type-aware C function that does the work using the C++ template:

.. code::

    #include <vector>

    using namespace std;

    extern "C" {
        void py_vector_int_new() {
            return new vector<int>();

        }
    }
"""
import os
from ctypes import cdll, c_void_p, c_size_t, c_int, c_long


def here(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


lib = cdll.LoadLibrary(here('_pystl.so'))


class Vector(object):

    def __init__(self, collection=None, ref=None, managed=None):
        """Initialize a vector adapter and optionally populate it.

        :param collection: An `iterable` which would be consumed and copied.
        :param ref: `void *` to an existing vector object. Passing this
         argument will prevent from allocating a new vector object.
        :param managed: Wether the vector reference should be deleted at the
        end of the adapter's life.

        Default behaviour is to allocate a new vector and delete it at object
        disposal time.

        If `ref` is given, default behaviour is to **not** to free the
        reference, unless `managed` is overriden set.

        This might be useful to pass the reference later on to C code. First
        allocate/populate a new vector or manipulate an existing one through
        `ref`, set `managed` to `False` and then access directly to the `void`
        pointer in `self.vector` to send the reference somewhere else.
        """
        self.managed = ref is None if managed is None else managed
        self.vector = ref or self.vector_new()

        if collection is not None:
            self.extend(collection)

    def __del__(self):
        if self.managed:
            self.vector_delete(self.vector)

    def __len__(self):
        return self.vector_size(self.vector)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in self._getslice(index)]
        return self.vector_at(self.vector, self._index(index))

    def __setitem__(self, index, value):
        self.vector_set(self.vector, self._index(index), value)

    def __iter__(self):
        return (self[i] for i in xrange(len(self)))

    def __delitem__(self, index):
        if isinstance(index, slice):
            size = len(self)
            if size == 0:
                return

            start, stop, step = self._resolve_iterator_slice(index, size)
            self.vector_erase_slice(self.vector, start, stop)
        else:
            self.vector_erase(self.vector, self._index(index))

    def __contains__(self, value):
        return self.vector_find(self.vector, value) != -1

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return bool(self.vector_equal(self.vector, other.vector))

    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return False
        return not (self == other)

    def __repr__(self):
        return u"[" + u", ".join(repr(i) for i in self) + u"]"

    def __str__(self):
        return repr(self)

    def insert(self, index, value):
        return self.vector_insert(self.vector, self._index(index), value)

    def append(self, value):
        self.vector_push_back(self.vector, value)

    def extend(self, collection):
        for item in collection:
            self.append(item)

    def index(self, value):
        index = self.vector_find(self.vector, value)
        if index < 0:
            raise ValueError(repr(value) + " is not in vector")
        return index

    def pop(self, index=None):
        if len(self) == 0:
            raise IndexError('pop from empty vector')

        if index is None:
            return self._pop_last()
        else:
            return self._pop_index(index)

    def _pop_last(self):
        return self.vector_pop_back(self.vector)

    def _pop_index(self, index):
        value = self[index]
        del self[index]
        return value

    def remove(self, value):
        del self[self.index(value)]

    def count(self, value):
        return self.vector_count(self.vector, value)

    def sort(self):
        self.vector_sort(self.vector)

    def reverse(self):
        self.vector_reverse(self.vector)

    def _resolve_negative_index(self, index, size):
        return index if index >= 0 else size + index

    def _check_index_boundaries(self, index, size):
        if index < 0 or index >= size:
            raise IndexError(u'Vector index {} out of range'.format(index))

    def _index(self, index):
        size = len(self)
        index = self._resolve_negative_index(index, size)
        self._check_index_boundaries(index, size)
        return index

    def _init_slice(self, sliced, size):
        """Get (start, stop, step) from a python sliced object"""
        start = 0 if sliced.start is None else sliced.start
        stop = size if sliced.stop is None else sliced.stop
        step = 1 if sliced.step is None else sliced.step

        start = self._resolve_negative_index(start, size)
        stop = self._resolve_negative_index(stop, size)

        return start, stop, step

    def _resolve_iterator_slice(self, sliced, size):
        """Compute indexes [begin, end) for a cpp iterator loop"""
        start, stop, step = self._init_slice(sliced, size)

        # assure boundaries
        start = max(0, min(start, size))
        stop = max(0, min(stop, size))

        # assure order
        if start > stop:
            start, stop = stop, start

        return start, stop, step

    def _resolve_slice(self, sliced, size):
        """Compute indexes [begin, end) for a range python call"""
        start, stop, step = self._init_slice(sliced, size)

        # assure boundaries
        # corner case for start: range(size, x) --> index error
        # corner case for stop: range(x, size) --> missing last value
        start = max(0, min(start, size - 1))
        stop = max(-1, min(stop, size))

        return start, stop, step

    def _getslice(self, sliced):
        size = len(self)

        if size == 0:
            return []

        start, stop, step = self._resolve_slice(sliced, size)

        return xrange(start, stop, step)


class VectorInt(Vector):

    vector_new = lib.py_vector_int_new
    vector_new.restype = c_void_p
    vector_new.argtypes = []

    vector_delete = lib.py_vector_int_delete
    vector_delete.restype = None
    vector_delete.argtypes = [c_void_p]

    vector_size = lib.py_vector_int_size
    vector_size.restype = c_size_t
    vector_size.argtypes = [c_void_p]

    vector_at = lib.py_vector_int_at
    vector_at.restype = c_int
    vector_at.argtypes = [c_void_p, c_size_t]

    vector_set = lib.py_vector_int_set
    vector_set.restype = None
    vector_set.argtypes = [c_void_p, c_size_t, c_int]

    vector_push_back = lib.py_vector_int_push_back
    vector_push_back.restype = None
    vector_push_back.argtypes = [c_void_p, c_int]

    vector_insert = lib.py_vector_int_insert
    vector_insert.restype = None
    vector_insert.argtypes = [c_void_p, c_size_t, c_int]

    vector_erase = lib.py_vector_int_erase
    vector_erase.restype = None
    vector_erase.argtypes = [c_void_p, c_size_t]

    vector_erase_slice = lib.py_vector_int_erase_slice
    vector_erase_slice.restype = None
    vector_erase_slice.argtypes = [c_void_p, c_size_t, c_size_t]

    vector_find = lib.py_vector_int_find
    vector_find.restype = c_int
    vector_find.argtypes = [c_void_p, c_int]

    vector_pop_back = lib.py_vector_int_pop_back
    vector_pop_back.restype = c_int
    vector_pop_back.argtypes = [c_void_p]

    vector_count = lib.py_vector_int_count
    vector_count.restype = c_int
    vector_count.argtypes = [c_void_p, c_int]

    vector_sort = lib.py_vector_int_sort
    vector_sort.restype = c_void_p
    vector_sort.argtypes = [c_void_p]

    vector_reverse = lib.py_vector_int_reverse
    vector_reverse.restype = c_void_p
    vector_reverse.argtypes = [c_void_p]

    vector_equal = lib.py_vector_int_equal
    vector_equal.restype = c_int
    vector_equal.argtypes = [c_void_p, c_void_p]


class VectorLong(Vector):

    vector_new = lib.py_vector_long_new
    vector_new.restype = c_void_p
    vector_new.argtypes = []

    vector_delete = lib.py_vector_long_delete
    vector_delete.restype = None
    vector_delete.argtypes = [c_void_p]

    vector_size = lib.py_vector_long_size
    vector_size.restype = c_size_t
    vector_size.argtypes = [c_void_p]

    vector_at = lib.py_vector_long_at
    vector_at.restype = c_long
    vector_at.argtypes = [c_void_p, c_size_t]

    vector_set = lib.py_vector_long_set
    vector_set.restype = None
    vector_set.argtypes = [c_void_p, c_size_t, c_long]

    vector_push_back = lib.py_vector_long_push_back
    vector_push_back.restype = None
    vector_push_back.argtypes = [c_void_p, c_long]

    vector_insert = lib.py_vector_long_insert
    vector_insert.restype = None
    vector_insert.argtypes = [c_void_p, c_size_t, c_long]

    vector_erase = lib.py_vector_long_erase
    vector_erase.restype = None
    vector_erase.argtypes = [c_void_p, c_size_t]

    vector_erase_slice = lib.py_vector_long_erase_slice
    vector_erase_slice.restype = None
    vector_erase_slice.argtypes = [c_void_p, c_size_t, c_size_t]

    vector_find = lib.py_vector_long_find
    vector_find.restype = c_int
    vector_find.argtypes = [c_void_p, c_long]

    vector_pop_back = lib.py_vector_long_pop_back
    vector_pop_back.restype = c_long
    vector_pop_back.argtypes = [c_void_p]

    vector_count = lib.py_vector_long_count
    vector_count.restype = c_size_t
    vector_count.argtypes = [c_void_p, c_long]

    vector_sort = lib.py_vector_long_sort
    vector_sort.restype = c_void_p
    vector_sort.argtypes = [c_void_p]

    vector_reverse = lib.py_vector_long_reverse
    vector_reverse.restype = c_void_p
    vector_reverse.argtypes = [c_void_p]

    vector_equal = lib.py_vector_long_equal
    vector_equal.restype = c_int
    vector_equal.argtypes = [c_void_p, c_void_p]
