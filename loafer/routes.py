import logging

from .message_translators import AbstractMessageTranslator
from .providers import AbstractProvider
from .utils import run_in_loop_or_executor

logger = logging.getLogger(__name__)


class Route:

    def __init__(self, provider, handler, name='default',
                 message_translator=None, error_handler=None):
        self.name = name

        if not isinstance(provider, AbstractProvider):
            raise TypeError('invalid provider instance: {!r}'.format(provider))

        self.provider = provider

        if message_translator:
            if not isinstance(message_translator, AbstractMessageTranslator):
                raise TypeError(
                    'invalid message translator instance: {!r}'.format(message_translator)
                )

        self.message_translator = message_translator

        if error_handler:
            if not callable(error_handler):
                raise TypeError(
                    'error_handler must be a callable object: {!r}'.format(error_handler)
                )

        self._error_handler = error_handler

        if callable(handler):
            self.handler = handler
            self._handler_instance = None
        else:
            self.handler = getattr(handler, 'handle', None)
            self._handler_instance = handler

        if not self.handler:
            raise ValueError(
                'handler must be a callable object or implement `handle` method: {!r}'.format(self.handler)
            )

    def __str__(self):
        return '<{}(name={} provider={!r} handler={!r})>'.format(
            type(self).__name__, self.name, self.provider, self.handler)

    def apply_message_translator(self, message):
        processed_message = {'content': message,
                             'metadata': {}}
        if not self.message_translator:
            return processed_message

        translated = self.message_translator.translate(processed_message['content'])
        processed_message['metadata'].update(translated.get('metadata', {}))
        processed_message['content'] = translated['content']
        if not processed_message['content']:
            raise ValueError('{} failed to translate message={}'.format(self.message_translator, message))

        return processed_message

    async def deliver(self, raw_message):
        message = self.apply_message_translator(raw_message)
        logger.info('delivering message route={}, message={!r}'.format(self, message))
        return await run_in_loop_or_executor(self.handler, message['content'], message['metadata'])

    async def error_handler(self, exc_info, message):
        logger.info('error handler process originated by message={}'.format(message))

        if self._error_handler is not None:
            return await run_in_loop_or_executor(self._error_handler, exc_info, message)

        return False

    def stop(self):
        logger.info('stopping route {}'.format(self))
        self.provider.stop()
        # only for class-based handlers
        if hasattr(self._handler_instance, 'stop'):
            self._handler_instance.stop()
