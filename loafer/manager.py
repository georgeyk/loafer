# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import signal

from consumer import AsyncSQSConsumer

logger = logging.getLogger(__name__)


class LoaferManager(object):

    def __init__(self, max_jobs=5):
        self._max_jobs = max_jobs

        self._loop = asyncio.get_event_loop()
        self._loop.add_signal_handler(signal.SIGINT, self.stop)
        self._loop.add_signal_handler(signal.SIGTERM, self.stop)

        # see https://github.com/python/asyncio/issues/258
        # reuse pool of 5 (asyncio default)
        self._executor = ThreadPoolExecutor(5)
        self._loop.set_default_executor(self._executor)
        self._loop.set_debug(True)

    def start(self):
        logger.info('Starting Loafer (pid={}) ...'.format(os.getpid()))

        self._consumer = AsyncSQSConsumer(self._max_jobs)
        self._future = asyncio.gather(self._consumer.consume(self._loop))

        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def stop(self, *args, **kwargs):
        logger.debug('Stopping Loafer ...')
        self._future.cancel()
        self._executor.shutdown(wait=True)
        self._loop.stop()


def main():
    loafer = LoaferManager()
    loafer.start()


if __name__ == '__main__':
    main()
