from loafer.ext.aws.message_translators import SNSMessageTranslator, SQSMessageTranslator
from loafer.ext.aws.providers import SQSProvider
from loafer.ext.aws.routes import SNSQueueRoute, SQSRoute


def test_sqs_route(dummy_handler):
    route = SQSRoute('what', handler=dummy_handler)
    assert isinstance(route.message_translator, SQSMessageTranslator)
    assert isinstance(route.provider, SQSProvider)
    assert route.name == 'what'


def test_sqs_route_keep_message_translator(dummy_handler):
    route = SQSRoute('what', handler=dummy_handler, message_translator=SNSMessageTranslator())
    assert isinstance(route.message_translator, SNSMessageTranslator)
    route = SQSRoute('what', handler=dummy_handler, message_translator=None)
    assert route.message_translator is None


def test_sqs_route_keep_name(dummy_handler):
    route = SQSRoute('what', handler=dummy_handler, name='foobar')
    assert route.name == 'foobar'


def test_sqs_route_provider_options(dummy_handler):
    route = SQSRoute('what', {'use_ssl': False}, handler=dummy_handler, name='foobar')
    assert 'use_ssl' in route.provider._client_options
    assert route.provider._client_options['use_ssl'] is False


def test_sns_queue_route(dummy_handler):
    route = SNSQueueRoute('what', handler=dummy_handler)
    assert isinstance(route.message_translator, SNSMessageTranslator)
    assert isinstance(route.provider, SQSProvider)
    assert route.name == 'what'


def test_sns_queue_route_keep_message_translator(dummy_handler):
    route = SNSQueueRoute('what', handler=dummy_handler, message_translator=SQSMessageTranslator())
    assert isinstance(route.message_translator, SQSMessageTranslator)
    route = SNSQueueRoute('what', handler=dummy_handler, message_translator=None)
    assert route.message_translator is None


def test_sns_queue_route_keep_name(dummy_handler):
    route = SNSQueueRoute('what', handler=dummy_handler, name='foobar')
    assert route.name == 'foobar'


def test_sns_queue_route_provider_options(dummy_handler):
    route = SNSQueueRoute('what', provider_options={'region_name': 'sa-east-1'}, handler=dummy_handler, name='foobar')
    assert 'region_name' in route.provider._client_options
    assert route.provider._client_options['region_name'] == 'sa-east-1'
