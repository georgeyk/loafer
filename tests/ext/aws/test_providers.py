from unittest import mock

from botocore.exceptions import ClientError

import pytest

from loafer.exceptions import ProviderError
from loafer.ext.aws.providers import SQSProvider


@pytest.mark.asyncio
async def test_get_queue_url(mock_boto_session_sqs, boto_client_sqs):
    with mock_boto_session_sqs as mock_sqs:
        consumer = SQSProvider('queue-name')
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
        consumer = SQSProvider('queue-name')
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
        consumer = SQSProvider('queue-name', options=options)
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
    boto_client_sqs.receive_message.return_value = {'Messages': []}
    with mock_boto_session_sqs:
        consumer = SQSProvider('queue-name', options=options)
        messages = await consumer.fetch_messages()

        assert messages == []

        assert boto_client_sqs.receive_message.call_args == mock.call(
            QueueUrl=await consumer.get_queue_url(),
            WaitTimeSeconds=options.get('WaitTimeSeconds'),
            MaxNumberOfMessages=options.get('MaxNumberOfMessages'))


@pytest.mark.asyncio
async def test_fetch_messages_with_client_error(mock_boto_session_sqs, boto_client_sqs):
    with mock_boto_session_sqs:
        error = ClientError(error_response={'Error': {'Message': 'unknown'}},
                            operation_name='whatever')
        boto_client_sqs.receive_message.side_effect = error

        provider = SQSProvider('queue-name')
        with pytest.raises(ProviderError):
            await provider.fetch_messages()
