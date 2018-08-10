import json
from unittest import mock

import pytest
from asynctest import CoroutineMock

from loafer.ext.aws.handlers import SNSHandler, SQSHandler

# SQSHandler


@pytest.mark.asyncio
@pytest.mark.parametrize('encoder', [json.dumps, str])
async def test_sqs_handler_publish(mock_boto_session_sqs, boto_client_sqs, encoder):
    handler = SQSHandler('queue-name')
    with mock_boto_session_sqs as mock_sqs:
        retval = await handler.publish('message', encoder=encoder)
        assert retval

        assert mock_sqs.called
        assert boto_client_sqs.send_message.called
        assert boto_client_sqs.send_message.call_args == mock.call(
            QueueUrl=await handler.get_queue_url('queue-name'),
            MessageBody=encoder('message'))


@pytest.mark.asyncio
async def test_sqs_handler_publish_without_encoder(mock_boto_session_sqs, boto_client_sqs):
    handler = SQSHandler('queue-name')
    with mock_boto_session_sqs as mock_sqs:
        retval = await handler.publish('message', encoder=None)
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
@pytest.mark.parametrize('encoder', [json.dumps, str])
async def test_sns_handler_publisher(mock_boto_session_sns, boto_client_sns, encoder):
    handler = SNSHandler('arn:aws:sns:whatever:topic-name')
    with mock_boto_session_sns as mock_sns:
        retval = await handler.publish('message', encoder=encoder)
        assert retval

        assert mock_sns.called
        assert boto_client_sns.publish.called
        assert boto_client_sns.publish.call_args == mock.call(
            TopicArn='arn:aws:sns:whatever:topic-name',
            MessageStructure='json',
            Message=json.dumps({'default': encoder('message')}))


@pytest.mark.asyncio
async def test_sns_handler_publisher_without_encoder(mock_boto_session_sns, boto_client_sns):
    handler = SNSHandler('arn:aws:sns:whatever:topic-name')
    with mock_boto_session_sns as mock_sns:
        retval = await handler.publish('message', encoder=None)
        assert retval

        assert mock_sns.called
        assert boto_client_sns.publish.called
        assert boto_client_sns.publish.call_args == mock.call(
            TopicArn='arn:aws:sns:whatever:topic-name',
            MessageStructure='json',
            Message=json.dumps({'default': 'message'}))


@pytest.mark.asyncio
async def test_sns_handler_publish_without_topic():
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
