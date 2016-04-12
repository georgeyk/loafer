# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from unittest import mock

import pytest

from loafer.aws.consumer import Consumer


@pytest.mark.asyncio
async def test_get_queue_url(mock_boto_client_sqs, mock_get_queue_url):
    with mock_boto_client_sqs as mock_sqs:
        consumer = Consumer('queue-name')
        queue_url = await consumer.get_queue_url()
        assert queue_url.startswith('https://')
        assert queue_url.endswith('queue-name')

        assert mock_sqs.called
        assert mock_sqs.called_once_with('sqs')
        assert mock_get_queue_url.called
        assert mock_get_queue_url.called_once_with(QueueName='queue-name')


@pytest.mark.asyncio
async def test_confirm_message(mock_boto_client_sqs_with_delete_message, mock_delete_message):
    with mock_boto_client_sqs_with_delete_message:
        consumer = Consumer('queue-name')
        queue_url = await consumer.get_queue_url()
        await consumer.confirm_message('message-receipt-handle')

        assert mock_delete_message.called_once_with(
            QueueUrl=queue_url,
            ReceiptHandle='message-receipt-handle')


@pytest.mark.asyncio
@mock.patch('loafer.aws.consumer.settings',
            return_value=mock.Mock(SQS_WAIT_TIME_SECONDS=5, SQS_MAX_MESSAGES=10))
async def test_fetch_messages(patched_settings, mock_boto_client_sqs_with_messages,
                              mock_receive_message):
    with mock_boto_client_sqs_with_messages:
        consumer = Consumer('queue-name')
        messages = await consumer.fetch_messages()

        assert len(messages) == 1
        assert messages[0]['Body'] == 'test'

        assert mock_receive_message.called_once_with(
            QueueUrl=await consumer.get_queue_url(),
            WaitTimeSeconds=patched_settings.SQS_WAIT_TIME_SECONDS,
            MaxNumberOfMessages=patched_settings.SQS_MAX_MESSAGES)


@pytest.mark.asyncio
@mock.patch('loafer.aws.consumer.settings',
            return_value=mock.Mock(SQS_WAIT_TIME_SECONDS=5, SQS_MAX_MESSAGES=10))
async def test_fetch_messages_returns_empty(patched_settings,
                                            mock_boto_client_sqs_with_empty_messages,
                                            mock_receive_message_empty):
    with mock_boto_client_sqs_with_empty_messages:
        consumer = Consumer('queue-name')
        messages = await consumer.fetch_messages()

        assert messages == []

        assert mock_receive_message_empty.called_once_with(
            QueueUrl=await consumer.get_queue_url(),
            WaitTimeSeconds=patched_settings.SQS_WAIT_TIME_SECONDS,
            MaxNumberOfMessages=patched_settings.SQS_MAX_MESSAGES)
