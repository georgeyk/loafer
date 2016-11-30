# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest import mock

import pytest

from loafer.message_translator import StringMessageTranslator
from loafer.routes import Route


def test_handler_property():
    route = Route('foo-queue', 'examples.jobs.example_job')
    assert callable(route.handler)

    route = Route('foo-queue', 'examples.jobs.async_example_job')
    assert callable(route.handler)


def test_handle_property_errors():
    route = Route('foo-queue', 'invalid_job')
    with pytest.raises(ImportError):
        route.handler

    route = Route('foo-queue', 'examples')
    with pytest.raises(ImportError):
        route.handler


def test_handler_name_property():
    route = Route('foo-queue', 'examples.jobs.example_job')
    assert route.handler_name == 'examples.jobs.example_job'


def test_source():
    route = Route(source='foo-queue', handler='invalid_job')
    assert route.source == 'foo-queue'


def test_name():
    route = Route(source='foo-queue', handler='invalid_job', name='foo')
    assert route.name == 'foo'


def test_message_translator():
    route = Route('foo', 'invalid', message_translator='unittest.mock.Mock')
    assert isinstance(route.message_translator, mock.Mock)


def test_default_message_translator():
    route = Route('foo', 'invalid')
    translator = route.message_translator
    assert isinstance(translator, StringMessageTranslator)


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
