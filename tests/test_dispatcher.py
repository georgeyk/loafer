# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest.mock import Mock

from asynctest import CoroutineMock
from asynctest import Mock as AsyncMock  # flake8: NOQA
import pytest

from loafer.exceptions import RejectMessage, IgnoreMessage
from loafer.dispatcher import LoaferDispatcher


def test_without_consumers(route):
    dispatcher = LoaferDispatcher(routes=[route])
    assert dispatcher.consumers == []
    assert len(dispatcher.consumers) == 0


def test_with_consumers(route):
    consumer = Mock()
    dispatcher = LoaferDispatcher(routes=[route], consumers=[consumer])
    assert len(dispatcher.consumers) == 1
    assert dispatcher.consumers[0] is consumer


def test_get_consumer_default(route):
    dispatcher = LoaferDispatcher(routes=[route])
    consumer = dispatcher.get_consumer(route)
    assert consumer is None


def test_get_consumer_custom(route):
    consumer = Mock(source=route.source)
    dispatcher = LoaferDispatcher(routes=[route], consumers=[consumer])
    returned_consumer = dispatcher.get_consumer(route)

    assert returned_consumer
    assert returned_consumer is consumer


def test_get_consumer_default_with_custom(route):
    consumer = Mock(source='other-source')
    dispatcher = LoaferDispatcher(routes=[route], consumers=[consumer])
    returned_consumer = dispatcher.get_consumer(route)

    assert returned_consumer is not consumer


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
async def test_dispatch_message_task_reject_message(route):
    route.deliver = CoroutineMock(side_effect=RejectMessage)
    dispatcher = LoaferDispatcher([route])

    message = 'rejected-message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is True

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_task_ignore_message(route):
    route.deliver = CoroutineMock(side_effect=IgnoreMessage)
    dispatcher = LoaferDispatcher([route])

    message = 'ignored-message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_message_task_error(route):
    route.deliver = CoroutineMock(side_effect=Exception)
    dispatcher = LoaferDispatcher([route])

    message = 'message'
    confirmation = await dispatcher.dispatch_message(message, route)
    assert confirmation is False

    assert route.message_translator.translate.called
    assert route.deliver.called
    assert route.deliver.called_once_with(message)


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
async def test_dispatch_consumers(route, consumer):
    routes = [route]
    dispatcher = LoaferDispatcher(routes)
    dispatcher.dispatch_message = CoroutineMock()
    dispatcher.get_consumer = Mock(return_value=consumer)

    # consumers will stop after the first iteration
    running_values = [False, True]

    def stopper():
        return running_values.pop(0)

    await dispatcher.dispatch_consumers(stopper)

    assert dispatcher.get_consumer.called
    assert dispatcher.get_consumer.called_once_with(route)
    assert consumer.consume.called

    assert dispatcher.dispatch_message.called
    assert dispatcher.dispatch_message.called_called_once_with('message', route)

    assert consumer.confirm_message.called
    assert consumer.confirm_message.called_once_with('message')
