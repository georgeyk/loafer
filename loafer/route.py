# -*- coding: utf-8 -*-

import asyncio
import logging

from cached_property import cached_property

from .conf import settings
from .utils import import_callable


logger = logging.getLogger(__name__)


class Route(object):

    def __init__(self, source, handler, name='default', message_translator=None):
        self.name = name
        self.source = source
        self._handler = handler
        self._message_translator = message_translator

    def __str__(self):
        return '<Route(name={} queue={} handler={})>'.format(
            self.name, self.source, self._handler)

    @cached_property
    def message_translator(self):
        if self._message_translator:
            return self._message_translator()
        klass = import_callable(settings.LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS)
        return klass()

    @cached_property
    def handler(self):
        return import_callable(self._handler)

    async def deliver(self, content, loop=None):
        logger.info('Delivering message content to handler={}'.format(self.handler))

        if asyncio.iscoroutinefunction(self.handler):
            logger.debug('Handler is coroutine! {!r}'.format(self.handler))
            return await self.handler(content)
        else:
            logger.debug('Handler will run in a separate thread: {!r}'.format(self.handler))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.handler, content)
