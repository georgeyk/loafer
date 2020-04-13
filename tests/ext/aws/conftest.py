from unittest import mock

import pytest
from asynctest import CoroutineMock

# boto client methods mock


@pytest.fixture
def queue_url():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/queue-name'
    return {'QueueUrl': queue_url}


@pytest.fixture
def sqs_message():
    message = {'Body': 'test'}
    return {'Messages': [message]}


def sqs_send_message():
    return {'MessageId': 'uuid', 'MD5OfMessageBody': 'md5',
            'ResponseMetada': {'RequestId': 'uuid', 'HTTPStatusCode': 200}}


@pytest.fixture
def sns_list_topics():
    return {'Topics': [{'TopicArn': 'arn:aws:sns:region:id:topic-name'}]}


@pytest.fixture
def sns_publish():
    return {'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'uuid'},
            'MessageId': 'uuid'}


# boto client mock


class ClientContextCreator:
    def __init__(self, client):
        self._client = client

    async def __aenter__(self):
        return self._client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def boto_client_sqs(queue_url, sqs_message):
    mock_client = mock.Mock()
    mock_client.get_queue_url = CoroutineMock(return_value=queue_url)
    mock_client.delete_message = CoroutineMock()
    mock_client.receive_message = CoroutineMock(return_value=sqs_message)
    mock_client.send_message = CoroutineMock(return_value=sqs_send_message)
    mock_client.close = CoroutineMock()
    return mock_client


@pytest.fixture
def mock_boto_session_sqs(boto_client_sqs):
    mock_session = mock.Mock()
    mock_session.create_client.return_value = ClientContextCreator(boto_client_sqs)
    return mock.patch('aiobotocore.get_session', return_value=mock_session)


@pytest.fixture
def boto_client_sns(sns_publish, sns_list_topics):
    mock_client = mock.Mock()
    mock_client.publish = CoroutineMock(return_value=sns_publish)
    mock_client.close = CoroutineMock()
    return mock_client


@pytest.fixture
def mock_boto_session_sns(boto_client_sns):
    mock_session = mock.Mock()
    mock_session.create_client.return_value = ClientContextCreator(boto_client_sns)
    return mock.patch('aiobotocore.get_session', return_value=mock_session)
