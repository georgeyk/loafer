# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest import mock

import pytest

from loafer.exceptions import ConfigurationError, ConsumerError
from loafer.dispatcher import LoaferDispatcher
from loafer.manager import LoaferManager
from loafer.route import Route

from loafer.aws.consumer import Consumer as AWSConsumer


def test_manager_with_no_routes(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    assert len(manager.routes) == 0


def test_manager_one_route(event_loop):
    route = Route('test-queue', lambda x: None)
    manager = LoaferManager('test-queue', event_loop=event_loop)
    manager.routes.append(route)

    assert len(manager.routes) == 1


def test_routes_stop_manager_if_loop_is_running(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    manager.stop = mock.Mock()

    with mock.patch.object(event_loop, 'is_running', return_value=True):
        with pytest.raises(ConfigurationError):
            manager.routes

        assert manager.stop.called
        assert manager.stop.called_once_with()


def test_consumers(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    assert manager.consumers
    assert len(manager.consumers) == 1


def test_consumers_returns_default_if_not_manually_set(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    assert manager.consumers[0].__class__ == AWSConsumer


def test_dispatcher(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    manager.get_dispatcher()
    assert manager._dispatcher
    assert isinstance(manager._dispatcher, LoaferDispatcher)


def test_on_future_errors(event_loop):
    manager = LoaferManager('test-queue', event_loop=event_loop)
    manager.stop = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ConsumerError)
    manager.on_future__errors(future)

    assert manager.stop.called
    assert manager.stop.called_once_with()
