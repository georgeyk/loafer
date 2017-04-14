from unittest import mock

import pytest

from loafer.ext.aws.bases import BaseSQSClient, BaseSNSClient


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


@pytest.fixture
def base_sns_client():
    return BaseSNSClient()


@pytest.mark.asyncio
async def test_get_topic_arn(mock_boto_session_sns, boto_client_sns, base_sns_client):
    with mock_boto_session_sns as mock_sns:
        arn = await base_sns_client.get_topic_arn('topic-name')
        assert arn.startswith('arn:')
        assert arn.endswith('topic-name')

        assert mock_sns.called
        assert mock_sns.called_once_with('sns')
        assert boto_client_sns.list_topics.called
        assert boto_client_sns.called_once_with()


@pytest.mark.asyncio
async def test_cache_get_topic_arn(mock_boto_session_sns, boto_client_sns, base_sns_client):
    with mock_boto_session_sns:
        await base_sns_client.get_topic_arn('topic-name')
        arn = await base_sns_client.get_topic_arn('topic-name')
        assert arn.startswith('arn:')
        assert arn.endswith('topic-name')
        assert boto_client_sns.list_topics.call_count == 1
