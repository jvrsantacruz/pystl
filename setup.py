# -*- coding: utf-8 -*-

from setuptools import setup, Extension


setup(
    name="pystl",
    version="0.0.1",
    description="Simple C++ STL ctypes wrapper",
    author="Javier Santacruz",
    author_email="javier.santacruz.lc@gmail.com",
    url="http://github.com/jvrsantacruz/pystl",
    license="LGPL",
    packages=['pystl'],
    ext_modules=[
        Extension(
            "pystl._pystl",
            sources=['pystl/vector.cpp'],
            include_dirs=['pystl'],
            language="c++"
        )
    ],
    platforms=['any'],
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)"
    ]
)
