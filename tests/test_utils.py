# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import inspect

import pytest

from loafer.utils import import_callable


def test_import_function():
    func = import_callable('loafer.utils.import_callable')
    assert callable(func)
    assert inspect.isfunction(func)


def test_import_class():
    klass = import_callable('loafer.exceptions.ConsumerError')
    assert klass.__name__ == 'ConsumerError'
    assert inspect.isclass(klass)


def test_error_on_method_name():
    with pytest.raises(ImportError):
        import_callable('unittest.mock.Mock.call_count')


def test_error_on_invalid_name():
    with pytest.raises(ImportError):
        import_callable('invalid-1234')
