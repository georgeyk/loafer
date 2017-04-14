from unittest import mock

from asynctest import CoroutineMock
import pytest


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


@pytest.fixture
def boto_client_sqs(queue_url, sqs_message):
    mock_client = CoroutineMock()
    mock_client.get_queue_url.return_value = queue_url
    mock_client.delete_message.return_value = mock.Mock()
    mock_client.receive_message.return_value = sqs_message
    mock_client.send_message.return_value = sqs_send_message
    return mock_client


@pytest.fixture
def mock_boto_session_sqs(boto_client_sqs):
    mock_session = mock.Mock()
    mock_session.create_client = mock.Mock(return_value=boto_client_sqs)
    return mock.patch('aiobotocore.get_session', return_value=mock_session)


@pytest.fixture
def boto_client_sns(sns_publish, sns_list_topics):
    mock_client = CoroutineMock()
    mock_client.list_topics.return_value = sns_list_topics
    mock_client.publish.return_value = sns_publish
    return mock_client


@pytest.fixture
def mock_boto_session_sns(boto_client_sns):
    mock_session = mock.Mock()
    mock_session.create_client = mock.Mock(return_value=boto_client_sns)
    return mock.patch('aiobotocore.get_session', return_value=mock_session)
