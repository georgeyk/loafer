# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from unittest import mock

from aiomock import AIOMock
import pytest


# boto client methods mock

@pytest.fixture
def queue_url():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/queue-name'
    return {'QueueUrl': queue_url}


@pytest.fixture
def mock_get_queue_url(queue_url):
    return mock.Mock(return_value={'QueueUrl': queue_url})


@pytest.fixture
def mock_message():
    message = {'Body': 'test'}
    return {'Messages': [message]}


@pytest.fixture
def mock_receive_message(mock_message):
    return mock.Mock(return_value=mock_message)


@pytest.fixture
def mock_send_message():
    response = {'MessageId': 'uuid', 'MD5OfMessageBody': 'md5',
                'ResponseMetada': {'RequestId': 'uuid', 'HTTPStatusCode': 200}}
    return mock.Mock(return_value=response)


@pytest.fixture
def mock_sns_list_topics():
    topics = {'Topics': [{'TopicArn': 'arn:aws:sns:region:id:topic-name'}]}
    return mock.Mock(return_value=topics)


@pytest.fixture
def mock_sns_publish():
    response = {'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'uuid'},
                'MessageId': 'uuid'}
    return mock.Mock(return_value=response)


# boto client mock


@pytest.fixture
def boto_client_sqs(queue_url, mock_message):
    mock_client = AIOMock()
    mock_client.get_queue_url.async_return_value = queue_url
    mock_client.delete_message.async_return_value = mock.Mock()
    mock_client.receive_message.async_return_value = mock_message
    return mock_client


@pytest.fixture
def mock_boto_session(boto_client_sqs):
    mock_session = mock.Mock()
    mock_session.create_client = mock.Mock(return_value=boto_client_sqs)
    return mock_session


@pytest.fixture
def mock_boto_session_sqs(mock_boto_session):
    return mock.patch('aiobotocore.get_session', return_value=mock_boto_session)


@pytest.fixture
def mock_boto_sync_client_sns(mock_sns_publish, mock_sns_list_topics):
    mock_client = mock.Mock(publish=mock_sns_publish,
                            list_topics=mock_sns_list_topics)
    return mock.patch('boto3.client', return_value=mock_client)


@pytest.fixture
def mock_boto_sync_client_sqs(mock_get_queue_url, mock_send_message):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url,
                            send_message=mock_send_message)
    return mock.patch('boto3.client', return_value=mock_client)
