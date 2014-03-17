pystl
=====

Basic ctypes wrapper around C++ STL

```python
from pystl import VectorInt

>>> v = VectorInt()
>>> v
[]
>>> v.append(1)
>>> v
[1]
```

It currently implements `int` and `long` vector types using ctypes and `void *`.
This is done through an _adapter_ class which is capable of both creating a new `vector` or to handle an existing one.

```python
>>> created_vector = mylibrary.func_that_returns_vector()
>>> v = VectorInt(ref=created_vector)
>>> v.append([1, 2, 3])
>>> v
>>> [1, 2, 3]
>>> mylibrary.func_that_uses_a_vector(v.vector)
```

Most of the Python `list` interface has been implemented and tested.

Status
------

This small project started as a quick experiment and has grown a bit since. 
Keep in mind that this is not bound to be a complete wrapper around C++ STL, but more of a resource about how to handle such wrappers on your own.
