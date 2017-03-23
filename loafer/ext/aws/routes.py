from ...routes import Route
from .message_translators import SQSMessageTranslator, SNSMessageTranslator


class SQSRoute(Route):
    def __init__(self, *args, **kwargs):
        kwargs['message_translator'] = SQSMessageTranslator()
        super().__init__(*args, **kwargs)


class SNSQueueRoute(Route):
    def __init__(self, *args, **kwargs):
        kwargs['message_translator'] = SNSMessageTranslator()
        super().__init__(*args, **kwargs)
