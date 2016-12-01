import asyncio
from unittest import mock

import pytest

from loafer.conf import Settings
from loafer.exceptions import ConfigurationError, ConsumerError
from loafer.dispatcher import LoaferDispatcher
from loafer.manager import LoaferManager


@pytest.mark.asyncio
async def test_routes():
    manager = LoaferManager()
    assert manager.routes
    assert len(manager.routes) == 1
    # this value is set on envvar in pytest.ini
    assert manager.routes[0].name == 'test'


@pytest.mark.asyncio
async def test_routes_raise_error_if_not_configured():
    settings = Settings()
    settings.LOAFER_ROUTES = None

    with pytest.raises(ConfigurationError):
        manager = LoaferManager(settings)
        manager.routes

    settings.LOAFER_ROUTES = []

    with pytest.raises(ConfigurationError):
        manager = LoaferManager(settings)

        manager.routes


@pytest.mark.asyncio
async def test_routes_stop_manager_if_loop_is_running():
    settings = Settings()
    settings.LOAFER_ROUTES = None
    manager = LoaferManager(settings)
    manager.stop = mock.Mock()

    with mock.patch.object(manager._loop, 'is_running', return_value=True):
        with pytest.raises(ConfigurationError):
            manager.routes

        assert manager.stop.called
        assert manager.stop.called_once_with()


@pytest.mark.asyncio
async def test_consumers():
    manager = LoaferManager()
    assert manager.consumers
    assert len(manager.consumers) == 1


@pytest.mark.asyncio
async def test_consumers_returns_empty_if_not_configure():
    settings = Settings()
    settings.LOAFER_CONSUMERS = None
    manager = LoaferManager(settings)
    assert manager.consumers == []


@pytest.mark.asyncio
async def test_dispatcher():
    manager = LoaferManager()
    assert manager.dispatcher
    assert isinstance(manager.dispatcher, LoaferDispatcher)


@pytest.mark.asyncio
async def test_on_future_errors():
    manager = LoaferManager()
    manager.stop = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ConsumerError)
    manager.on_future__errors(future)

    assert manager.stop.called
    assert manager.stop.called_once_with()
