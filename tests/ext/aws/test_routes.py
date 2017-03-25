from unittest import mock

from loafer.ext.aws.message_translators import SQSMessageTranslator, SNSMessageTranslator
from loafer.ext.aws.providers import SQSProvider
from loafer.ext.aws.routes import SQSRoute, SNSQueueRoute


def test_sqs_route():
    route = SQSRoute('what', handler='ever')
    assert isinstance(route.message_translator, SQSMessageTranslator)
    assert isinstance(route.provider, SQSProvider)
    assert route.name == 'what'


def test_sqs_route_keep_message_translator():
    route = SQSRoute('what', handler='ever', message_translator=mock.Mock())
    assert isinstance(route.message_translator, mock.Mock)


def test_sqs_route_keep_name():
    route = SQSRoute('what', handler='ever', name='foobar')
    assert route.name == 'foobar'


def test_sns_queue_route():
    route = SNSQueueRoute('what', handler='ever')
    assert isinstance(route.message_translator, SNSMessageTranslator)
    assert isinstance(route.provider, SQSProvider)
    assert route.name == 'what'


def test_sns_queue_route_keep_message_translator():
    route = SNSQueueRoute('what', handler='ever', message_translator=mock.Mock())
    assert isinstance(route.message_translator, mock.Mock)


def test_sns_queue_route_keep_name():
    route = SNSQueueRoute('what', handler='ever', name='foobar')
    assert route.name == 'foobar'
