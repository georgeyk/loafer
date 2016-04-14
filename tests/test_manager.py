# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest import mock

import pytest

from loafer.conf import Settings
from loafer.exceptions import ConfigurationError, ConsumerError
from loafer.dispatcher import LoaferDispatcher
from loafer.manager import LoaferManager


def test_routes(event_loop):
    manager = LoaferManager()
    assert manager.routes
    assert len(manager.routes) == 1
    # this value is set on envvar in pytest.ini
    assert manager.routes[0].name == 'test'


def test_routes_raise_error_if_not_configured(event_loop):
    settings = Settings()
    settings.LOAFER_ROUTES = None

    with pytest.raises(ConfigurationError):
        manager = LoaferManager(settings)
        manager.routes

    settings.LOAFER_ROUTES = []

    with pytest.raises(ConfigurationError):
        manager = LoaferManager(settings)

        manager.routes


def test_routes_stop_manager_if_loop_is_running(event_loop):
    settings = Settings()
    settings.LOAFER_ROUTES = None
    manager = LoaferManager(settings)
    manager.stop = mock.Mock()

    with mock.patch.object(event_loop, 'is_running', return_value=True):
        with pytest.raises(ConfigurationError):
            manager.routes

        assert manager.stop.called
        assert manager.stop.called_once_with()


def test_consumers(event_loop):
    manager = LoaferManager()
    assert manager.consumers
    assert len(manager.consumers) == 1


def test_consumers_returns_empty_if_not_configure(event_loop):
    settings = Settings()
    settings.LOAFER_CONSUMERS = None
    manager = LoaferManager(settings)
    assert manager.consumers == []


def test_dispatcher(event_loop):
    manager = LoaferManager()
    assert manager.dispatcher
    assert isinstance(manager.dispatcher, LoaferDispatcher)


def test_on_future_errors(event_loop):
    manager = LoaferManager()
    manager.stop = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ConsumerError)
    manager.on_future__errors(future)

    assert manager.stop.called
    assert manager.stop.called_once_with()
