import logging
from copy import copy

from cached_property import cached_property

from .conditions import Retry
from .message_translators import AbstractMessageTranslator
from .providers import AbstractProvider
from .utils import run_in_loop_or_executor

logger = logging.getLogger(__name__)


class Route:

    def __init__(self, provider, handler, name='default',
                 message_translator=None, error_handler=None, conditions=None):
        self.name = name
        self._conditions = conditions or []

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

    @cached_property
    def _retry(self):
        for condition in self._conditions:
            if isinstance(condition, Retry):
                return condition

    async def fetch_messages(self):
        return await self.provider.fetch_messages()

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

    async def _deliver(self, raw_message):
        message = self.apply_message_translator(raw_message)
        logger.info('delivering message route={}, message={!r}'.format(self, message))
        return await run_in_loop_or_executor(self.handler, message['content'], message['metadata'])

    async def deliver(self, raw_message):
        if self._retry:
            retry = copy(self._retry)  # retry must be individual to each message
            return await retry.deliver(self, raw_message)

        return await self._deliver(raw_message)

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
