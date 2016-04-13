# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

import pytest

from loafer.conf import Settings


@pytest.fixture
def default_settings():
    return Settings()


def test_configuration_from_env():
    os.environ['LOAFER_LOG_FORMAT'] = 'whatever'
    settings = Settings()
    settings.LOAFER_LOG_FORMAT == 'whatever'


def test_configuration_has_defaults(default_settings):
    # XXX: add more keys wit default values
    assert default_settings.LOAFER_LOGLEVEL == 'WARNING'


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
