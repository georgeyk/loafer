# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from asynctest import CoroutineMock
from asynctest import Mock as AsyncMock  # flake8: NOQA
import pytest

from loafer.route import Route
from loafer.dispatcher import LoaferDispatcher


@pytest.fixture
def consumer_consume_mock():
    return CoroutineMock(consume=CoroutineMock(return_value=['message']))


@pytest.fixture
def route(consumer_consume_mock):
    get_consumer_mock = AsyncMock(return_value=consumer_consume_mock)
    route = AsyncMock(queue_name='queue', handler='handler',
                      get_consumer=get_consumer_mock,
                      confirm_message=CoroutineMock(),
                      spec=Route)
    return route


@pytest.mark.asyncio
async def test_dispatch_message(route):
    route.deliver = CoroutineMock(return_value='receipt')
    routes = [route]
    dispatcher = LoaferDispatcher(routes)
    message = 'foobar'

    await dispatcher.dispatch_message(message, route)

    assert route.deliver.called
    assert route.deliver.called_once_with('foobar')
    assert route.confirm_message.called
    assert route.confirm_message.called_once_with('receipt')


@pytest.mark.asyncio
async def test_dispatch_message_without_confirmation(route):
    route.deliver = CoroutineMock(return_value=None)
    routes = [route]
    dispatcher = LoaferDispatcher(routes)
    message = 'foobar'

    await dispatcher.dispatch_message(message, route)

    assert route.deliver.called
    assert route.deliver.called_once_with('foobar')
    assert not route.confirm_message.called


@pytest.mark.asyncio
async def test_dispatch_consumers(route):
    routes = [route]
    dispatcher = LoaferDispatcher(routes)
    dispatcher.dispatch_message = CoroutineMock()

    # consumers will stop after the first iteration
    running_values = [False, True]

    def stopper():
        return running_values.pop(0)

    await dispatcher.dispatch_consumers(stopper)

    assert route.get_consumer.called
    assert route.get_consumer().consume.called
    assert dispatcher.dispatch_message.called
    assert dispatcher.dispatch_message.called_called_once_with('message', route)
