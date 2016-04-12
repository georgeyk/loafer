# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from unittest import mock

import pytest

from loafer.route import Route


def test_get_queue_url(mock_boto_client_sqs, mock_get_queue_url):
    with mock_boto_client_sqs as mock_sqs:
        route = Route('queue-name', 'whatever')
        assert route.queue_url.startswith('https://')
        assert route.queue_url.endswith('queue-name')

        assert mock_sqs.called
        assert mock_sqs.called_once_with('sqs')
        assert mock_get_queue_url.called
        assert mock_get_queue_url.called_once_with(QueueName='queue-name')


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


# FIXME: Improve all test_deliver* tests

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


@pytest.mark.asyncio
@mock.patch('loafer.route.settings',
            return_value=mock.Mock(SQS_WAIT_TIME_SECONDS=5, SQS_MAX_MESSAGES=10))
async def test_fetch_messages_returns_empty(patched_settings,
                                            mock_boto_client_sqs_with_empty_messages,
                                            mock_receive_message_empty):
    with mock_boto_client_sqs_with_empty_messages:
        route = Route('queue-name', 'loafer.jobs.example_job')
        messages = await route.fetch_messages()

        assert messages == []

        assert mock_receive_message_empty.called_once_with(
            QueueUrl=route.queue_url,
            WaitTimeSeconds=patched_settings.SQS_WAIT_TIME_SECONDS,
            MaxNumberOfMessages=patched_settings.SQS_MAX_MESSAGES)


@pytest.mark.asyncio
@mock.patch('loafer.route.settings',
            return_value=mock.Mock(SQS_WAIT_TIME_SECONDS=5, SQS_MAX_MESSAGES=10))
async def test_fetch_messages(patched_settings, mock_boto_client_sqs_with_messages,
                              mock_receive_message):
    with mock_boto_client_sqs_with_messages:
        route = Route('queue-name', 'loafer.jobs.example_job')
        messages = await route.fetch_messages()

        assert len(messages) == 1
        assert messages[0]['Body'] == 'test'

        assert mock_receive_message.called_once_with(
            QueueUrl=route.queue_url,
            WaitTimeSeconds=patched_settings.SQS_WAIT_TIME_SECONDS,
            MaxNumberOfMessages=patched_settings.SQS_MAX_MESSAGES)
