# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import logging

from .conf import settings
from .utils import import_callable

logger = logging.getLogger(__name__)


class LoaferDispatcher(object):

    def __init__(self, routes, consumers=None):
        self.routes = routes
        self.consumers = consumers or []
        self._semaphore = asyncio.Semaphore(settings.LOAFER_MAX_JOBS)
        self._stopped_consumers = True

    def get_consumer(self, route):
        for consumer in self.consumers:
            if consumer.source == route.source:
                return consumer

        # no consumer for given route, return default
        klass = import_callable(settings.LOAFER_DEFAULT_CONSUMER_CLASS)
        options = settings.LOAFER_DEFAULT_CONSUMER_OPTIONS
        return klass(route.source, options)

    async def dispatch_message(self, message, route):
        logger.info('Dispatching message to route={}'.format(route))
        logger.debug('Dispatching message: {!r}'.format(message))

        # in the future, we may change the route depending on message content
        content = route.message_translator.translate(message)

        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            # TODO: handle errors here
            await route.deliver(content)

        return message

    async def dispatch_consumers(self, stopper=None):
        if stopper is None:
            self._stopped_consumers = False
            stopper = self._stopper

        while not stopper():
            for route in self.routes:
                consumer = self.get_consumer(route)
                messages = await consumer.consume()
                for message in messages:
                    confirmation = await self.dispatch_message(message, route)
                    if confirmation:
                        await consumer.confirm_message(message)

    def _stopper(self):
        return self._stopped_consumers

    def stop_consumers(self):
        logger.info('Stopping consumers')
        self._stopped_consumers = True
