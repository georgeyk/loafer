# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import logging

from .exceptions import RejectMessage, IgnoreMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher(object):
    def __init__(self, routes, consumers=None, max_jobs=10):
        self.routes = routes
        self.consumers = consumers or []
        self.max_jobs = max_jobs
        self._semaphore = asyncio.Semaphore(self.max_jobs)
        self._stop_consumers = True

        self.consumers_sources = dict((x.source, x) for x in self.consumers)

    def get_consumer(self, route):
        consumer = self.consumers_sources.get(route.source)
        return consumer

    def translate_message(self, message, route):
        try:
            content = route.message_translator.translate(message)['content']
        except Exception as exc:
            logger.exception(exc)
            logger.error('Error translating message content')
            return None

        return content

    async def dispatch_message(self, message, route):  # NOQA
        logger.info('Dispatching message to route={}'.format(route))

        content = self.translate_message(message, route)
        if content is None:
            logger.warning('Message will be ignored:\n{}\n'.format(message))
            return False

        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            try:
                await route.deliver(content)
            except RejectMessage as exc:
                logger.exception(exc)
                logger.warning('Explicit message rejection:\n{}\n'.format(message))
                # eg, we will return True at the end
            except IgnoreMessage as exc:
                logger.exception(exc)
                logger.warning('Explicit message ignore:\n{}\n'.format(message))
                return False
            except asyncio.CancelledError as exc:
                msg = '"{}" was cancelled, the message will be ignored:\n{}\n'
                logger.warning(msg.format(route.handler_name, message))
                return False
            except Exception as exc:
                logger.exception(exc)
                logger.error('Unhandled exception on {}'.format(route.handler_name))
                return False

        return True

    async def dispatch_consumers(self, sentinel=None):
        if sentinel is None or not callable(sentinel):
            self._stop_consumers = False
            stopper = self._default_sentinel
        else:
            stopper = sentinel

        while not stopper():
            for route in self.routes:
                consumer = self.get_consumer(route)
                messages = await consumer.consume()
                for message in messages:
                    confirmation = await self.dispatch_message(message, route)
                    if confirmation:
                        await consumer.confirm_message(message)

    def _default_sentinel(self):
        return self._stop_consumers

    def stop_consumers(self):
        logger.info('Stopping consumers')
        self._stop_consumers = True
