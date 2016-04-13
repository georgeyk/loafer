# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

from loafer.conf import Settings


def test_configuration_from_env():
    os.environ['LOAFER_LOG_FORMAT'] = 'whatever'
    settings = Settings()
    settings.LOAFER_LOG_FORMAT == 'whatever'


def test_configuration_has_defaults():
    # XXX: add more keys wit default values
    # Make sure key does not exist in env
    if 'LOAFER_LOGLEVEL' in os.environ:
        del os.environ['LOAFER_LOGLEVEL']

    settings = Settings()
    # the value does matter, it exists
    assert settings.LOAFER_LOGLEVEL


def test_override_env_configuration():
    os.environ['LOAFER_LOG_FORMAT'] = 'foobar'
    settings = Settings(LOAFER_LOG_FORMAT='overriden')
    assert settings.LOAFER_LOG_FORMAT == 'overriden'


def test_ignore_lower_keys():
    settings = Settings(foobar=2)
    assert not hasattr(settings, 'foobar')


def test_ignore_if_miss_loafer_prefix():
    settings = Settings(LOAFER_FOO=1, WITHOUT_PREFIX=2)
    assert hasattr(settings, 'LOAFER_FOO')
    assert settings.LOAFER_FOO == 1
    assert not hasattr(settings, 'WITHOUT_PREFIX')
