from unittest import mock

import pytest

from loafer.ext.aws.bases import BaseSNSClient, BaseSQSClient


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


@pytest.mark.asyncio
async def test_sqs_close(mock_boto_session_sqs, base_sqs_client, boto_client_sqs):
    with mock_boto_session_sqs:
        await base_sqs_client.stop()
        boto_client_sqs.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_sqs_get_client(mock_boto_session_sqs, base_sqs_client, boto_client_sqs):
    with mock_boto_session_sqs as mock_session:
        client_generator = base_sqs_client.get_client()
        assert mock_session.called
        async with client_generator as client:
            assert boto_client_sqs is client


@pytest.fixture
def base_sns_client():
    return BaseSNSClient()


@pytest.mark.asyncio
async def test_get_topic_arn_using_topic_name(base_sns_client):
    arn = await base_sns_client.get_topic_arn('topic-name')
    assert arn == 'arn:aws:sns:*:topic-name'


@pytest.mark.asyncio
async def test_cache_get_topic_arn_with_arn(base_sns_client):
    arn = await base_sns_client.get_topic_arn('arn:aws:sns:whatever:topic-name')
    assert arn == 'arn:aws:sns:whatever:topic-name'


@pytest.mark.asyncio
async def test_sns_close(mock_boto_session_sns, base_sns_client, boto_client_sns):
    with mock_boto_session_sns:
        await base_sns_client.stop()
        boto_client_sns.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_sns_get_client(mock_boto_session_sns, base_sns_client, boto_client_sns):
    with mock_boto_session_sns as mock_session:
        client_generator = base_sns_client.get_client()
        assert mock_session.called
        async with client_generator as client:
            assert boto_client_sns is client
