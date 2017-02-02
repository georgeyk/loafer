import asyncio
from unittest.mock import Mock

from asynctest import CoroutineMock
from asynctest import Mock as AsyncMock  # flake8: NOQA
import pytest

from loafer.exceptions import DeleteMessage, KeepMessage
from loafer.dispatcher import LoaferDispatcher
from loafer.routes import Route


@pytest.fixture
def provider():
    return CoroutineMock(fetch_messages=CoroutineMock(return_value=['message']),
                         source='queue',
                         confirm_message=CoroutineMock())


@pytest.fixture
def route(provider):
    message_translator = Mock(translate=Mock(return_value={'content': 'message'}))
    route = AsyncMock(provider=provider, handler='handler',
                      message_translator=message_translator, spec=Route)
    return route


@pytest.mark.asyncio
async def test_dispatch_message(route):
    route.deliver = CoroutineMock(return_value='receipt')
    dispatcher = LoaferDispatcher([route])

    message = 'foobar'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is True

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_without_translation(route):
    route.deliver = CoroutineMock(return_value=None)
    dispatcher = LoaferDispatcher([route])

    message = None
    route.message_translator.translate = Mock(return_value={'content': None})

    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert not route.deliver.called


@pytest.mark.asyncio
async def test_dispatch_message_error_on_translation(route):
    route.deliver = CoroutineMock(return_value=None)
    dispatcher = LoaferDispatcher([route])

    message = 'invalid-message'
    route.message_translator.translate = Mock(side_effect=Exception)

    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert not route.deliver.called


@pytest.mark.asyncio
async def test_dispatch_message_task_delete_message(route):
    route.deliver = CoroutineMock(side_effect=DeleteMessage)
    dispatcher = LoaferDispatcher([route])

    message = 'rejected-message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is True

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_task_ignore_message(route):
    route.deliver = CoroutineMock(side_effect=KeepMessage)
    dispatcher = LoaferDispatcher([route])

    message = 'ignored-message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_task_error(route):
    exc = Exception()
    route.deliver = CoroutineMock(side_effect=exc)
    route.error_handler = CoroutineMock(return_value=False)
    dispatcher = LoaferDispatcher([route])

    message = 'message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called is True
    assert route.deliver.called is True
    route.deliver.assert_called_once_with(message)
    assert route.error_handler.called is True
    route.error_handler.assert_called_once_with(type(exc), exc, message)


@pytest.mark.asyncio
async def test_dispatch_message_task_cancel(route):
    route.deliver = CoroutineMock(side_effect=asyncio.CancelledError)
    dispatcher = LoaferDispatcher([route])

    message = 'message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_process_route(route):
    dispatcher = LoaferDispatcher([route])
    dispatcher.dispatch_message = CoroutineMock()
    await dispatcher.process_route(route)

    assert route.provider.fetch_messages.called
    assert dispatcher.dispatch_message.called
    assert dispatcher.dispatch_message.called_called_once_with('message', route)
    assert route.provider.confirm_message.called
    assert route.provider.confirm_message.called_once_with('message')
