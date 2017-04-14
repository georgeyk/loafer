import json
from unittest import mock

from asynctest import CoroutineMock
import pytest

from loafer.ext.aws.handlers import SQSHandler, SNSHandler


# SQSHandler

@pytest.mark.asyncio
async def test_sqs_handler_publish(mock_boto_session_sqs, boto_client_sqs):
    handler = SQSHandler('queue-name')
    with mock_boto_session_sqs as mock_sqs:
        retval = await handler.publish('message')
        assert retval

        assert mock_sqs.called
        assert boto_client_sqs.send_message.called
        assert boto_client_sqs.send_message.call_args == mock.call(
            QueueUrl=await handler.get_queue_url('queue-name'),
            MessageBody='message')


@pytest.mark.asyncio
async def test_sqs_handler_publish_without_queue_name():
    handler = SQSHandler()
    with pytest.raises(ValueError):
        await handler.publish('wrong')


@pytest.mark.asyncio
async def test_sqs_handler_hadle():
    handler = SQSHandler('foobar')
    handler.publish = CoroutineMock()
    await handler.handle('message', 'metadata')
    assert handler.publish.called
    assert handler.publish.called_once_with('message')


# SNSHandler

@pytest.mark.asyncio
async def test_sns_handler_publisher(mock_boto_session_sns, boto_client_sns):
    handler = SNSHandler('topic-name')
    with mock_boto_session_sns as mock_sns:
        retval = await handler.publish('message')
        assert retval

        assert mock_sns.called
        assert boto_client_sns.publish.called
        assert boto_client_sns.publish.call_args == mock.call(
            TopicArn=await handler.get_topic_arn('topic-name'),
            MessageStructure='json',
            Message=json.dumps({'default': 'message'}))


@pytest.mark.asyncio
async def test_sns_handler_publish_without_topic_name():
    handler = SNSHandler()
    with pytest.raises(ValueError):
        await handler.publish('wrong')


@pytest.mark.asyncio
async def test_sns_handler_hadle():
    handler = SNSHandler('foobar')
    handler.publish = CoroutineMock()
    await handler.handle('message', 'metadata')
    assert handler.publish.called
    assert handler.publish.called_once_with('message')
