import asyncio
import logging

from .aws.message_translator import SQSMessageTranslator

logger = logging.getLogger(__name__)


class Route(object):
    def __init__(self, source, message_handler, name='default', message_translator=None):
        self.name = name
        self.source = source
        self.message_handler = message_handler

        if message_translator is None:
            self.message_translator = SQSMessageTranslator()
        else:
            self.message_translator = message_translator

    def __str__(self):
        return '<Route(name={} queue={} message_handler={})>'.format(
            self.name, self.source, self.message_handler)

    async def deliver(self, content, loop=None):
        logger.info('Delivering message content to message_handler={}'.format(self.message_handler))

        if asyncio.iscoroutinefunction(self.message_handler):
            logger.debug('Handler is coroutine! {!r}'.format(self.message_handler))
            return await self.message_handler(content)
        else:
            logger.debug('Handler will run in a separate thread: {!r}'.format(self.message_handler))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.message_handler, content)
