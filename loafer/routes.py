import asyncio
import logging

from .message_translators import AbstractMessageTranslator
from .providers import AbstractProvider

logger = logging.getLogger(__name__)


class Route:

    def __init__(self, provider, handler, name='default',
                 message_translator=None, error_handler=None):
        self.name = name

        assert isinstance(provider, AbstractProvider), 'invalid provider instance'
        self.provider = provider

        self.message_translator = message_translator
        if message_translator:
            assert isinstance(message_translator, AbstractMessageTranslator), \
                'invalid message translator instance'

        self._error_handler = error_handler
        if error_handler:
            assert callable(error_handler), 'error_handler must be a callable object'

        if callable(handler):
            self.handler = handler
            self._handler_instance = None
        else:
            self.handler = getattr(handler, 'handle', None)
            self._handler_instance = handler

        assert self.handler, 'handler must be a callable object or implement `handle` method'

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

    async def deliver(self, raw_message, loop=None):
        message = self.apply_message_translator(raw_message)
        logger.info(
            'delivering message content to handler={!r}, message={!r}'.format(self.handler, message)
        )

        if asyncio.iscoroutinefunction(self.handler):
            logger.debug('handler is coroutine! {!r}'.format(self.handler))
            return await self.handler(message['content'], message['metadata'])
        else:
            logger.debug('handler will run in a separate thread: {!r}'.format(self.handler))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.handler, message['content'], message['metadata'])

    async def error_handler(self, exc_info, message, loop=None):
        logger.info('error handler process originated by message={}'.format(message))
        if self._error_handler is not None:
            if asyncio.iscoroutinefunction(self._error_handler):
                return await self._error_handler(exc_info, message)
            else:
                loop = loop or asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._error_handler, exc_info, message)

        return False

    def stop(self):
        logger.info('stopping route {}'.format(self))
        self.provider.stop()
        # only for class-based handlers
        if hasattr(self._handler_instance, 'stop'):
            self._handler_instance.stop()
