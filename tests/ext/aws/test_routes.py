from loafer.ext.aws.routes import SQSRoute, SNSQueueRoute
from loafer.ext.aws.message_translators import SQSMessageTranslator, SNSMessageTranslator


def test_sqs_route():
    route = SQSRoute('what', 'ever')
    assert isinstance(route.message_translator, SQSMessageTranslator)


def test_sns_queue_route():
    route = SNSQueueRoute('what', 'ever')
    assert isinstance(route.message_translator, SNSMessageTranslator)
