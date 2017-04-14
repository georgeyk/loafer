from unittest import mock

import pytest

from loafer.ext.aws.bases import BaseSQSClient


@pytest.fixture
def base_sqs_client():
    return BaseSQSClient()


@pytest.mark.asyncio
async def test_get_queue_url(mock_boto_session_sqs, boto_client_sqs, base_sqs_client):
    with mock_boto_session_sqs as mock_sqs:
        queue_url = await base_sqs_client.get_queue_url('queue-name')
        assert queue_url.startswith('https://')
        assert queue_url.endswith('queue-name')

        assert mock_sqs.called
        assert mock_sqs.called_once_with('sqs')
        assert boto_client_sqs.get_queue_url.called
        assert boto_client_sqs.get_queue_url.call_args == mock.call(QueueName='queue-name')


@pytest.mark.asyncio
async def test_cache_get_queue_url(mock_boto_session_sqs, boto_client_sqs, base_sqs_client):
    with mock_boto_session_sqs:
        await base_sqs_client.get_queue_url('queue-name')
        queue_url = await base_sqs_client.get_queue_url('queue-name')
        assert queue_url.startswith('https://')
        assert queue_url.endswith('queue-name')
        assert boto_client_sqs.get_queue_url.call_count == 1
