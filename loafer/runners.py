import asyncio
from concurrent.futures import ThreadPoolExecutor, CancelledError
import logging
import os
import signal

logger = logging.getLogger(__name__)


class LoaferRunner:
    def __init__(self, loop=None, max_workers=None, on_stop_callback=None):
        self._on_stop_callback = on_stop_callback
        self.loop = loop or asyncio.get_event_loop()

        # XXX: See https://github.com/python/asyncio/issues/258
        # The minimum value depends on the number of cores in the machine
        # See https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        self._executor = ThreadPoolExecutor(max_workers)
        self.loop.set_default_executor(self._executor)

    def start(self, future=None, run_forever=True):
        start = 'starting Loafer, pid={}, run_forever={}'
        logger.info(start.format(os.getpid(), run_forever))

        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        try:
            if run_forever:
                self.loop.run_forever()
            else:
                self.loop.run_until_complete(future)
                self.stop()
        except CancelledError:
            self.loop.close()

    def stop(self, *args, **kwargs):
        logger.info('stopping Loafer ...')
        if callable(self._on_stop_callback):
            self._on_stop_callback()

        self._executor.shutdown(wait=True)
        if self.loop.is_running():
            self.loop.stop()
