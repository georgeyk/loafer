# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal

from . import __version__
from .conf import settings
from .dispatcher import LoaferDispatcher
from .exceptions import ConsumerError
from .route import Route

logger = logging.getLogger(__name__)


class LoaferManager(object):

    def __init__(self, configuration=None):
        self._conf = configuration or settings

        self._loop = asyncio.get_event_loop()
        self._loop.add_signal_handler(signal.SIGINT, self.stop)
        self._loop.add_signal_handler(signal.SIGTERM, self.stop)

        # XXX: See https://github.com/python/asyncio/issues/258
        # The minimum value depends on the number of cores in the machine
        # See https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        self._executor = ThreadPoolExecutor(self._conf.LOAFER_MAX_THREAD_POOL)
        self._loop.set_default_executor(self._executor)

    def get_routes(self):
        if not self._conf.LOAFER_ROUTES:
            msg = 'Missing LOAFER_ROUTES configuration'
            logger.critical(msg)
            self.stop()
            raise ValueError(msg)

        routes = []
        for data in self._conf.LOAFER_ROUTES:
            routes.append(Route(data['source'], data['handler'], data['name']))

        return routes

    @property
    def dispatcher(self):
        routes = self.get_routes()
        return LoaferDispatcher(routes)

    def start(self, routes_values=None):
        start = 'Starting Loafer - Version: {} (pid={}) ...'
        logger.info(start.format(__version__, os.getpid()))

        self._future = asyncio.gather(self.dispatcher.dispatch_consumers())
        self._future.add_done_callback(self.on_future__errors)

        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def stop(self, *args, **kwargs):
        logger.info('Stopping Loafer ...')

        logger.debug('Stopping consumers ...')
        self.dispatcher.stop_consumers()

        logger.debug('Cancel schedulled operations ...')
        self._future.cancel()

        logger.debug('Waiting to shutdown ...')
        self._executor.shutdown(wait=True)
        self._loop.stop()

    def on_future__errors(self, future):
        exc = future.exception()
        if isinstance(exc, ConsumerError):
            logger.critical('Fatal error caught: {!r}'.format(exc))
            self.stop()
