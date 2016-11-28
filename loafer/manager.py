# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal

from cached_property import cached_property

from . import __version__
from .conf import settings
from .dispatcher import LoaferDispatcher
from .exceptions import ConfigurationError
from .route import Route
from .utils import import_callable

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

    @cached_property
    def routes(self):
        if not self._conf.LOAFER_ROUTES:
            msg = 'Missing LOAFER_ROUTES configuration'
            logger.critical(msg)
            if self._loop.is_running():
                self.stop()
            raise ConfigurationError(msg)

        routes = []
        for data in self._conf.LOAFER_ROUTES:
            message_translator = data.get('message_translator', None)
            routes.append(Route(data['source'], data['handler'], data['name'],
                                message_translator=message_translator))
        return routes

    @cached_property
    def consumers(self):
        if not self._conf.LOAFER_CONSUMERS:
            return []

        consumers = []
        for consumer_settings in self._conf.LOAFER_CONSUMERS:
            for source, consumer_data in consumer_settings.items():
                klass = import_callable(consumer_data.get('consumer_class'))
                options = consumer_data.get('consumer_options')
                consumers.append(klass(source, options))
        return consumers

    @cached_property
    def dispatcher(self):
        if self._conf.LOAFER_ROUTES:
            return LoaferDispatcher(self.routes, self.consumers)

    def start(self):
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
        if self.dispatcher:
            self.dispatcher.stop_consumers()

            logger.debug('Cancel schedulled operations ...')
            self._future.cancel()

        logger.debug('Waiting to shutdown ...')
        self._executor.shutdown(wait=True)
        self._loop.stop()

    def on_future__errors(self, future):
        exc = future.exception()
        # Unhandled errors crashes the event loop execution
        if isinstance(exc, BaseException):
            logger.critical('Fatal error caught: {!r}'.format(exc))
            self.stop()
