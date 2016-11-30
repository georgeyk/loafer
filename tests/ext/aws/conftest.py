# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from unittest import mock

import pytest


# boto client methods mock

@pytest.fixture
def mock_get_queue_url():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/queue-name'
    return mock.Mock(return_value={'QueueUrl': queue_url})


@pytest.fixture
def mock_receive_message_empty():
    return mock.Mock(return_value={})


@pytest.fixture
def mock_receive_message():
    message = {'Body': 'test'}
    return mock.Mock(return_value={'Messages': [message]})


@pytest.fixture
def mock_send_message():
    response = {'MessageId': 'uuid', 'MD5OfMessageBody': 'md5',
                'ResponseMetada': {'RequestId': 'uuid', 'HTTPStatusCode': 200}}
    return mock.Mock(return_value=response)


@pytest.fixture
def mock_delete_message():
    return mock.Mock()


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
def mock_boto_client_sns(mock_sns_publish, mock_sns_list_topics):
    mock_client = mock.Mock(publish=mock_sns_publish,
                            list_topics=mock_sns_list_topics)
    return mock.patch('boto3.client', return_value=mock_client)


@pytest.fixture
def mock_boto_client_sqs(mock_get_queue_url, mock_send_message):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url,
                            send_message=mock_send_message)
    return mock.patch('boto3.client', return_value=mock_client)


@pytest.fixture
def mock_boto_client_sqs_with_empty_messages(mock_get_queue_url,
                                             mock_receive_message_empty):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url,
                            receive_message=mock_receive_message_empty)
    return mock.patch('boto3.client', return_value=mock_client)


@pytest.fixture
def mock_boto_client_sqs_with_messages(mock_get_queue_url, mock_receive_message):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url,
                            receive_message=mock_receive_message)
    return mock.patch('boto3.client', return_value=mock_client)


@pytest.fixture
def mock_boto_client_sqs_with_delete_message(mock_get_queue_url, mock_delete_message):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url,
                            delete_message=mock_delete_message)
    return mock.patch('boto3.client', return_value=mock_client)
