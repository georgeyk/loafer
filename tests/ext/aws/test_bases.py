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


@pytest.mark.asyncio
async def test_get_queue_url_when_queue_name_is_url(mock_boto_session_sqs, boto_client_sqs, base_sqs_client):
    with mock_boto_session_sqs:
        queue_url = await base_sqs_client.get_queue_url('https://aws-whatever/queue-name')
        assert queue_url.startswith('https://')
        assert queue_url.endswith('queue-name')
        assert boto_client_sqs.get_queue_url.call_count == 0


def test_sqs_close(base_sqs_client):
    base_sqs_client.client = mock.Mock()
    base_sqs_client.stop()
    assert base_sqs_client.client.close.called


@pytest.fixture
def base_sns_client():
    return BaseSNSClient()


@pytest.mark.asyncio
async def test_get_topic_arn_using_topic_name(base_sns_client):
    arn = await base_sns_client.get_topic_arn('topic-name')
    assert arn == 'arn:sns:*:topic-name'


@pytest.mark.asyncio
async def test_cache_get_topic_arn_with_arn(base_sns_client):
    arn = await base_sns_client.get_topic_arn('arn:sns:whatever:topic-name')
    assert arn == 'arn:sns:whatever:topic-name'


def test_sns_close(base_sns_client):
    base_sns_client.client = mock.Mock()
    base_sns_client.stop()
    assert base_sns_client.client.close.called
