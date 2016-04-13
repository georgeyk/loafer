# -*- coding: utf-8 -*-

import asyncio
import logging

from cached_property import cached_property

from .conf import settings
from .utils import import_callable


logger = logging.getLogger(__name__)


class Route(object):

    def __init__(self, source, handler, name='default'):
        self.name = name
        self.source = source
        self._handler = handler

    def __str__(self):
        return '<Route(name={} queue={} handler={})>'.format(
            self.name, self.source, self._handler)

    def get_consumer_class(self):
        return import_callable(settings.LOAFER_DEFAULT_CONSUMER_CLASS)

    @cached_property
    def handler(self):
        return import_callable(self._handler)

    def get_consumer(self):
        klass = self.get_consumer_class()
        return klass(self.source, settings.LOAFER_DEFAULT_CONSUMER_OPTIONS)

    async def deliver(self, content, loop=None):
        if asyncio.iscoroutinefunction(self.handler):
            logger.info('Handler is coroutine! {!r}'.format(self.handler))
            return await self.handler(content)
        else:
            logger.info('Handler will run in a separate thread: {!r}'.format(self.handler))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.handler, content)
