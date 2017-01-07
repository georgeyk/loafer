import asyncio
from unittest import mock

from loafer.dispatcher import LoaferDispatcher
from loafer.exceptions import ProviderError
from loafer.managers import LoaferManager
from loafer.runners import LoaferRunner


def test_dispatcher():
    runner = LoaferRunner(loop=mock.Mock())
    manager = LoaferManager(routes=[], consumers=[], runner=runner)
    assert manager.dispatcher
    assert isinstance(manager.dispatcher, LoaferDispatcher)


def test_on_future_errors():
    manager = LoaferManager(routes=[], consumers=[])
    manager.runner = mock.Mock()
    future = asyncio.Future()
    future.set_exception(ProviderError)
    manager.on_future__errors(future)

    assert manager.runner.stop.called
    assert manager.runner.stop.called_once_with()


def test_on_loop__stop():
    manager = LoaferManager(routes=[], consumers=[])
    manager.dispatcher = mock.Mock()
    manager._future = mock.Mock()
    manager.on_loop__stop()

    assert manager.dispatcher.stop_providers.called
    assert manager._future.cancel.called
