# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import inspect
import os
import sys

import pytest

from loafer.utils import import_callable, add_current_dir_to_syspath


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

    with pytest.raises(ImportError):
        import_callable('')


def test_error_on_module():
    with pytest.raises(ImportError):
        import_callable('examples')


def test_error_on_non_callable():
    with pytest.raises(ImportError):
        import_callable('loafer')


@pytest.mark.xfail(os.getcwd() == '/tmp', run=False,
                   reason='This test is invalid if you are at /tmp')
def test_current_dir_in_syspath():
    old_current = os.getcwd()
    os.chdir('/tmp')
    current = os.getcwd()
    if current not in sys.path:
        sys.path.append(current)

    @add_current_dir_to_syspath
    def inner_test():
        assert current in sys.path

    inner_test()
    assert current in sys.path

    sys.path.remove(current)
    os.chdir(old_current)


@pytest.mark.xfail(os.getcwd() == '/tmp', run=False,
                   reason='This test is invalid if you are at /tmp')
def test_current_dir_not_in_syspath():
    old_current = os.getcwd()
    os.chdir('/tmp')
    current = os.getcwd()

    @add_current_dir_to_syspath
    def inner_test():
        assert current in sys.path

    inner_test()
    assert current not in sys.path

    os.chdir(old_current)
