import asyncio
import logging

logger = logging.getLogger(__name__)


class Route:
    def __init__(self, provider, handler, name='default',
                 message_translator=None, error_handler=None):
        self.name = name
        self.provider = provider
        self.message_translator = message_translator
        self.handler = handler
        self._error_handler = error_handler

    def __str__(self):
        return '<{}(name={} provider={!r} handler={!r})>'.format(
            type(self).__name__, self.name, self.provider, self._handler)

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
        logger.info('delivering message content to handler={!r}'.format(self.handler))

        if asyncio.iscoroutinefunction(self.handler):
            logger.debug('handler is coroutine! {!r}'.format(self.handler))
            return await self.handler(message['content'], message['metadata'])
        else:
            logger.debug('handler will run in a separate thread: {!r}'.format(self.handler))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.handler, message['content'], message['metadata'])

    async def error_handler(self, exc_type, exc, message, loop=None):
        if self._error_handler is not None:
            if asyncio.iscoroutinefunction(self._error_handler):
                return await self._error_handler(exc_type, exc, message)
            else:
                loop = loop or asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._error_handler, exc_type, exc, message)

        return False
