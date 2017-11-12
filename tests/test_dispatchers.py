import asyncio
from unittest.mock import Mock

from asynctest import CoroutineMock
from asynctest import Mock as AsyncMock  # flake8: NOQA
import pytest

from loafer.exceptions import DeleteMessage
from loafer.dispatchers import LoaferDispatcher
from loafer.routes import Route


@pytest.fixture
def provider():
    return CoroutineMock(fetch_messages=CoroutineMock(return_value=['message']),
                         confirm_message=CoroutineMock())


@pytest.fixture
def route(provider):
    message_translator = Mock(translate=Mock(return_value={'content': 'message'}))
    route = AsyncMock(provider=provider, handler=Mock(),
                      message_translator=message_translator,
                      enabled=True, spec=Route)
    return route


@pytest.mark.asyncio
async def test_dispatch_message(route):
    route.deliver = CoroutineMock(return_value='confirmation')
    dispatcher = LoaferDispatcher([route])

    message = 'foobar'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation == 'confirmation'

    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
@pytest.mark.parametrize('message', [None, ''])
async def test_dispatch_invalid_message(route, message):
    route.deliver = CoroutineMock()
    dispatcher = LoaferDispatcher([route])

    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False
    assert route.deliver.called is False


@pytest.mark.asyncio
async def test_dispatch_message_task_delete_message(route):
    route.deliver = CoroutineMock(side_effect=DeleteMessage)
    dispatcher = LoaferDispatcher([route])

    message = 'rejected-message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is True

    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_task_error(route):
    exc = Exception()
    route.deliver = CoroutineMock(side_effect=exc)
    route.error_handler = CoroutineMock(return_value='confirmation')
    dispatcher = LoaferDispatcher([route])

    message = 'message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation == 'confirmation'

    assert route.deliver.called is True
    route.deliver.assert_called_once_with(message)
    assert route.error_handler.called is True


@pytest.mark.asyncio
async def test_dispatch_message_task_cancel(route):
    route.deliver = CoroutineMock(side_effect=asyncio.CancelledError)
    dispatcher = LoaferDispatcher([route])

    message = 'message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_message_processing(route):
    dispatcher = LoaferDispatcher([route])
    dispatcher.dispatch_message = CoroutineMock()
    await dispatcher._process_message('message', route)

    assert dispatcher.dispatch_message.called
    assert dispatcher.dispatch_message.called_called_once_with('message', route)
    assert route.provider.confirm_message.called
    assert route.provider.confirm_message.called_once_with('message')


@pytest.mark.asyncio
async def test_dispatch_tasks(route, event_loop):
    route.provider.fetch_messages = CoroutineMock(return_value=['message'])
    dispatcher = LoaferDispatcher([route])
    dispatched = await dispatcher._dispatch_tasks(event_loop)

    assert len(dispatched) == 1
    assert route.provider.fetch_messages.called


@pytest.mark.asyncio
async def test_dispatch_without_tasks(route, event_loop):
    route.provider.fetch_messages = CoroutineMock(return_value=[])
    dispatcher = LoaferDispatcher([route])
    dispatched = await dispatcher._dispatch_tasks(event_loop)

    assert len(dispatched) == 0
    assert route.provider.fetch_messages.called


@pytest.mark.asyncio
async def test_dispatch_tasks_disabled(route, event_loop):
    route.enabled = False
    dispatcher = LoaferDispatcher([route])
    dispatched = await dispatcher._dispatch_tasks(event_loop)

    assert len(dispatched) == 0
    assert route.provider.fetch_messages.called is False


@pytest.mark.asyncio
async def test_dispatch_providers(route, event_loop):
    dispatcher = LoaferDispatcher([route])
    dispatcher._dispatch_tasks = CoroutineMock()
    dispatcher.stop_providers = Mock()
    await dispatcher.dispatch_providers(event_loop, forever=False)

    assert dispatcher._dispatch_tasks.called
    dispatcher._dispatch_tasks.assert_called_once_with(event_loop)


@pytest.mark.asyncio
async def test_dispatch_providers_with_error(route, event_loop):
    route.provider.fetch_messages.side_effect = ValueError
    dispatcher = LoaferDispatcher([route])
    with pytest.raises(ValueError):
        await dispatcher.dispatch_providers(event_loop, forever=False)


def test_dispatcher_stop(route):
    route.stop = Mock()
    dispatcher = LoaferDispatcher([route])
    dispatcher.stop()
    assert route.stop.called
