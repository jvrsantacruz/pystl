# -*- coding: utf-8 -*-

from contextlib import contextmanager


class Spy(object):
    def __init__(self, returns=None):
        self.returns = returns
        self.call_args = None
        self.call_kwargs = None
        self.number_of_calls = 0

    def __call__(self, *args, **kwargs):
        self.call_args = args
        self.call_kwargs = kwargs
        self.number_of_calls += 1
        return self.returns

    @property
    def called(self):
        return bool(self.number_of_calls)


@contextmanager
def raw_vector(v):
    cv = v.vector_new()
    try:
        yield cv
    finally:
        v.vector_delete(cv)


@contextmanager
def populated_raw_vector(v, collection):
    with raw_vector(v) as cv:
        for number in collection:
            v.vector_push_back(cv, number)
        yield cv


def patch(obj, **kwargs):
    for name, attr in kwargs.items():
        setattr(obj, name, attr)


@contextmanager
def patched(obj, **kwargs):
    previous = {name: getattr(obj, name) for name in kwargs}

    patch(kwargs)
    yield obj
    patch(previous)
