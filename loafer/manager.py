# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal

from . import __version__
from .dispatcher import LoaferDispatcher
from .aws.consumer import Consumer as AWSConsumer


logger = logging.getLogger(__name__)


class LoaferManager(object):

    def __init__(self, source, thread_pool_size=4):
        self._loop = asyncio.get_event_loop()
        self._loop.add_signal_handler(signal.SIGINT, self.stop)
        self._loop.add_signal_handler(signal.SIGTERM, self.stop)

        # XXX: See https://github.com/python/asyncio/issues/258
        # The minimum value depends on the number of cores in the machine
        # See https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        self.thread_pool_size = thread_pool_size
        self._executor = ThreadPoolExecutor(self.thread_pool_size)
        self._loop.set_default_executor(self._executor)

        self.routes = []
        self.consumers = [AWSConsumer(source, {'WaitTimeSeconds': 5, 'MaxNumberOfMessages': 5}, loop=self._loop)]
        self._dispatcher = None

    def get_dispatcher(self):
        return LoaferDispatcher(self.routes, self.consumers)

    def start(self):
        start_message = 'Starting Loafer - Version: {} (pid={}) ...'
        logger.info(start_message.format(__version__, os.getpid()))

        self._dispatcher = self.get_dispatcher()

        self._future = asyncio.gather(self._dispatcher.dispatch_consumers())
        self._future.add_done_callback(self.on_future__errors)

        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def stop(self, *args, **kwargs):
        logger.info('Stopping Loafer ...')

        logger.debug('Stopping consumers ...')
        self._dispatcher.stop_consumers()

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
