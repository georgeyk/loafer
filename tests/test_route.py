# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest import mock

import pytest

from loafer.aws.message_translator import SQSMessageTranslator
from loafer.route import Route
from loafer.example.jobs import example_job, async_example_job


def test_handler_property():
    route = Route('foo-queue', example_job)
    assert callable(route.message_handler)

    route = Route('foo-queue', async_example_job)
    assert callable(route.message_handler)


def test_source():
    route = Route('foo-queue', example_job)
    assert route.source == 'foo-queue'


def test_name():
    route = Route('foo-queue', example_job, name='foo')
    assert route.name == 'foo'


def test_message_translator():
    route = Route('foo', example_job, message_translator=mock.Mock())
    assert isinstance(route.message_translator, mock.Mock)


def test_default_message_translator():
    route = Route('foo', example_job)
    translator = route.message_translator
    assert isinstance(translator, SQSMessageTranslator)


# FIXME: Improve all test_deliver* tests

@pytest.mark.asyncio
async def test_deliver():

    mock_handler = mock.Mock()
    async def test_handler(*args, **kwargs):
        mock_handler(*args, **kwargs)

    route = Route('foo-queue', test_handler)

    await route.deliver('test')

    mock_handler.assert_called_once_with('test')
    assert asyncio.iscoroutinefunction(route.message_handler)


@pytest.mark.asyncio
async def test_deliver_with_coroutine():

    attrs = {}

    async def test_handler(*args, **kwargs):
        attrs['args'] = args
        attrs['kwargs'] = kwargs

    route = Route('foo-queue', 'will.be.patched')
    # monkey-patch
    route.message_handler = test_handler

    message = 'test'
    await route.deliver(message)

    assert message in attrs['args']
    assert asyncio.iscoroutinefunction(route.message_handler)
