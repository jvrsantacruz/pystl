pystl
=====

Basic ctypes wrapper around C++ STL

[![](https://travis-ci.org/jvrsantacruz/pystl.png?branch=master)](https://travis-ci.org/jvrsantacruz/pystl)

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

Development
-----------

Tests are written using `nose` and different environments are managed by using `tox`.

So, to install the application in development mode and run the tests:

```shell
$ virtualenv pystl
$ pystl/env/activate
(pystl)$ tox
```

Status
------

This small project started as a quick experiment and has grown a bit since. 
Keep in mind that this is not bound to be a complete wrapper around C++ STL, but more of a resource about how to handle such wrappers on your own.
