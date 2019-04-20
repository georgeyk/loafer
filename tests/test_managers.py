import asyncio
from unittest import mock

import pytest

from loafer.dispatchers import LoaferDispatcher
from loafer.exceptions import ConfigurationError, ProviderError
from loafer.managers import LoaferManager
from loafer.routes import Route
from loafer.runners import LoaferRunner


@pytest.fixture
def dummy_route(dummy_provider):
    return Route(dummy_provider, handler=mock.Mock())


def test_dispatcher_invalid_routes():
    manager = LoaferManager(routes=[])
    with pytest.raises(ConfigurationError):
        manager.dispatcher


def test_dispatcher_invalid_route_instance():
    manager = LoaferManager(routes=[mock.Mock()])
    with pytest.raises(ConfigurationError):
        manager.dispatcher


def test_dispatcher(dummy_route):
    manager = LoaferManager(routes=[dummy_route])
    assert manager.dispatcher
    assert isinstance(manager.dispatcher, LoaferDispatcher)


def test_default_runner():
    manager = LoaferManager(routes=[])
    assert manager.runner
    assert isinstance(manager.runner, LoaferRunner)


def test_custom_runner():
    runner = mock.Mock()
    manager = LoaferManager(routes=[], runner=runner)
    assert manager.runner
    assert isinstance(manager.runner, mock.Mock)


def test_on_future_errors():
    manager = LoaferManager(routes=[])
    manager.runner = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ProviderError)
    manager.on_future__errors(future)

    assert manager.runner.prepare_stop.called
    assert manager.runner.prepare_stop.called_once_with()


def test_on_future_errors_cancelled():
    manager = LoaferManager(routes=[])
    manager.runner = mock.Mock()
    future = asyncio.Future()
    future.cancel()
    manager.on_future__errors(future)

    assert manager.runner.prepare_stop.called
    assert manager.runner.prepare_stop.called_once_with()


def test_on_loop__stop():
    manager = LoaferManager(routes=[])
    manager.dispatcher = mock.Mock()
    manager._future = mock.Mock()
    manager.on_loop__stop()

    assert manager.dispatcher.stop.called
    assert manager._future.cancel.called
