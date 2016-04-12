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


# boto client mock

@pytest.fixture
def mock_boto_client_sqs(mock_get_queue_url):
    mock_client = mock.Mock(get_queue_url=mock_get_queue_url)
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
