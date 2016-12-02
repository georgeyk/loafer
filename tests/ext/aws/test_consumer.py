from unittest import mock

from botocore.exceptions import ClientError

import pytest

from loafer.exceptions import ConsumerError
from loafer.ext.aws.consumer import Consumer


@pytest.mark.asyncio
async def test_get_queue_url(mock_boto_session_sqs, boto_client_sqs):
    with mock_boto_session_sqs as mock_sqs:
        consumer = Consumer('queue-name')
        queue_url = await consumer.get_queue_url()
        assert queue_url.startswith('https://')
        assert queue_url.endswith('queue-name')

        assert mock_sqs.called
        assert mock_sqs.called_once_with('sqs')
        assert boto_client_sqs.get_queue_url.called
        assert boto_client_sqs.get_queue_url.call_args == mock.call(QueueName='queue-name')


@pytest.mark.asyncio
async def test_confirm_message(mock_boto_session_sqs, boto_client_sqs):
    with mock_boto_session_sqs:
        consumer = Consumer('queue-name')
        queue_url = await consumer.get_queue_url()
        message = {'ReceiptHandle': 'message-receipt-handle'}
        await consumer.confirm_message(message)

        assert boto_client_sqs.delete_message.call_args == mock.call(
            QueueUrl=queue_url,
            ReceiptHandle='message-receipt-handle')


@pytest.mark.asyncio
async def test_fetch_messages(mock_boto_session_sqs, boto_client_sqs):
    options = {'WaitTimeSeconds': 5, 'MaxNumberOfMessages': 10}
    with mock_boto_session_sqs:
        consumer = Consumer('queue-name', options=options)
        messages = await consumer.fetch_messages()

        assert len(messages) == 1
        assert messages[0]['Body'] == 'test'

        assert boto_client_sqs.receive_message.call_args == mock.call(
            QueueUrl=await consumer.get_queue_url(),
            WaitTimeSeconds=options.get('WaitTimeSeconds'),
            MaxNumberOfMessages=options.get('MaxNumberOfMessages'))


@pytest.mark.asyncio
async def test_fetch_messages_returns_empty(mock_boto_session_sqs, boto_client_sqs):
    options = {'WaitTimeSeconds': 5, 'MaxNumberOfMessages': 10}
    boto_client_sqs.receive_message.async_return_value = {'Messages': []}
    with mock_boto_session_sqs:
        consumer = Consumer('queue-name', options=options)
        messages = await consumer.fetch_messages()

        assert messages == []

        assert boto_client_sqs.receive_message.call_args == mock.call(
            QueueUrl=await consumer.get_queue_url(),
            WaitTimeSeconds=options.get('WaitTimeSeconds'),
            MaxNumberOfMessages=options.get('MaxNumberOfMessages'))


@pytest.mark.asyncio
async def test_consume(mock_boto_session_sqs, boto_client_sqs):
    boto_client_sqs.receive_message.async_return_value = {'Messages': []}
    with mock_boto_session_sqs:
        consumer = Consumer('queue-name')
        messages = await consumer.consume()
        assert messages == []

        queue_url = await boto_client_sqs.get_queue_url()
        assert boto_client_sqs.receive_message.called
        assert boto_client_sqs.receive_message.call_args == mock.call(QueueUrl=queue_url['QueueUrl'])


@pytest.mark.asyncio
async def test_consume_with_client_error(mock_boto_session_sqs):
    with mock_boto_session_sqs as mock_sqs:
        error = ClientError(error_response={'Error': {'Message': 'unknown'}},
                            operation_name='whatever')
        mock_sqs.side_effect = error

        consumer = Consumer('queue-name')
        with pytest.raises(ConsumerError):
            await consumer.consume()
