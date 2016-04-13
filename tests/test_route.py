# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio

import pytest

from loafer.route import Route


def test_handler_property():
    route = Route('foo-queue', 'loafer.jobs.example_job')
    assert callable(route.handler)

    route = Route('foo-queue', 'loafer.jobs.async_example_job')
    assert callable(route.handler)


def test_handle_property_errors():
    route = Route('foo-queue', 'invalid_job')
    with pytest.raises(ImportError):
        route.handler

    route = Route('foo-queue', 'loafer.jobs')
    with pytest.raises(ImportError):
        route.handler


def test_queue_name():
    route = Route('foo-queue', 'invalid_job')
    assert route.queue_name == 'foo-queue'


def test_get_consumer():
    class CustomConsumer(object):
        def __init__(self, queue, options=None):
            self.queue = queue

    route = Route('foo-queue', 'invalid_job')
    route.get_consumer_class = lambda: CustomConsumer
    consumer = route.get_consumer()

    assert consumer.queue == 'foo-queue'
    assert isinstance(consumer, CustomConsumer)


# FIXME: Improve all test_deliver* tests

@pytest.mark.asyncio
async def test_deliver():

    attrs = {}

    def test_handler(*args, **kwargs):
        attrs['args'] = args
        attrs['kwargs'] = kwargs

    route = Route('foo-queue', 'will.be.patched')
    # monkey-patch
    route.handler = test_handler

    message = 'test'
    await route.deliver(message)

    assert message in attrs['args']
    assert not asyncio.iscoroutinefunction(route.handler)


@pytest.mark.asyncio
async def test_deliver_with_coroutine():

    attrs = {}

    async def test_handler(*args, **kwargs):
        attrs['args'] = args
        attrs['kwargs'] = kwargs

    route = Route('foo-queue', 'will.be.patched')
    # monkey-patch
    route.handler = test_handler

    message = 'test'
    await route.deliver(message)

    assert message in attrs['args']
    assert asyncio.iscoroutinefunction(route.handler)
