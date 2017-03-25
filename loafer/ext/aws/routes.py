from ...routes import Route
from .providers import SQSProvider
from .message_translators import SQSMessageTranslator, SNSMessageTranslator


class SQSRoute(Route):
    def __init__(self, provider_queue, provider_options=None, *args, **kwargs):
        provider_options = provider_options or {}
        provider = SQSProvider(provider_queue, **provider_options)
        kwargs['provider'] = provider
        if not kwargs.get('message_translator', False):
            kwargs['message_translator'] = SQSMessageTranslator()
        if not kwargs.get('name', False):
            kwargs['name'] = provider_queue

        super().__init__(*args, **kwargs)


class SNSQueueRoute(Route):
    def __init__(self, provider_queue, provider_options=None, *args, **kwargs):
        provider_options = provider_options or {}
        provider = SQSProvider(provider_queue, **provider_options)
        kwargs['provider'] = provider
        if not kwargs.get('message_translator', False):
            kwargs['message_translator'] = SNSMessageTranslator()
        if not kwargs.get('name', False):
            kwargs['name'] = provider_queue

        super().__init__(*args, **kwargs)
