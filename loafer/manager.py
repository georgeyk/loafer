# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal

from .conf import settings
from .dispatcher import LoaferDispatcher
from .exceptions import ConsumerError
from .route import Route

logger = logging.getLogger(__name__)


class LoaferManager(object):

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._loop.add_signal_handler(signal.SIGINT, self.stop)
        self._loop.add_signal_handler(signal.SIGTERM, self.stop)

        # XXX: See https://github.com/python/asyncio/issues/258
        # The minimum value depends on the number of cores in the machine
        # See https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        self._executor = ThreadPoolExecutor(settings.MAX_THREAD_POOL)
        self._loop.set_default_executor(self._executor)

    def get_routes(self, routes_values=None):
        routes = []
        if routes_values is None:
            if not settings.LOAFER_ROUTES:
                self.stop()
                raise ValueError('Missing LOUFER_ROUTES configuration')
        else:
            for queue, handler in routes_values:
                routes.append(Route(queue, handler))

        # direct parameters takes precedence over configuration
        if not routes:
            for queue, handler in settings.LOAFER_ROUTES:
                routes.append(Route(queue, handler))

        return routes

    def start(self, routes_values=None):
        logger.info('Starting Loafer (pid={}) ...'.format(os.getpid()))

        routes = self.get_routes(routes_values)
        self._dispatcher = LoaferDispatcher(routes)
        self._future = asyncio.gather(self._dispatcher.dispatch_consumers())
        self._future.add_done_callback(self.on_future__errors)

        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def stop(self, *args, **kwargs):
        self._dispatcher.stop_consumers()
        self._future.cancel()
        self._executor.shutdown(wait=True)
        self._loop.stop()
        logger.info('Stopping Loafer ...')

    def on_future__errors(self, future):
        exc = future.exception()
        if isinstance(exc, ConsumerError):
            logger.error('Fatal error caught: {!r}'.format(exc))
            self.stop()
