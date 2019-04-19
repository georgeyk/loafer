import asyncio
import logging
import signal
from concurrent.futures import CancelledError, ThreadPoolExecutor
from contextlib import suppress

logger = logging.getLogger(__name__)


class LoaferRunner:

    def __init__(self, max_workers=None, on_stop_callback=None):
        self._on_stop_callback = on_stop_callback

        # XXX: See https://github.com/python/asyncio/issues/258
        # The minimum value depends on the number of cores in the machine
        # See https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        self._executor = ThreadPoolExecutor(max_workers)
        self.loop.set_default_executor(self._executor)

    @property
    def loop(self):
        return asyncio.get_event_loop()

    def start(self, future=None, run_forever=None, debug=False):
        if debug:
            self.loop.set_debug(enabled=debug)

        if future:
            logger.warning(
                'runner `future` argument is deprecated and will be removed in the next major version'
            )
        if run_forever:
            logger.warning(
                'runner `run_forever` argument is deprecated and will be removed in the next major version'
            )

        self.loop.add_signal_handler(signal.SIGINT, self.prepare_stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.prepare_stop)

        try:
            self.loop.run_forever()
        finally:
            self.stop()
            self.loop.close()
            logger.debug('loop.is_running={}'.format(self.loop.is_running()))
            logger.debug('loop.is_closed={}'.format(self.loop.is_closed()))

    def prepare_stop(self, *args):
        if self.loop.is_running():
            # signals loop.run_forever to exit in the next iteration
            self.loop.stop()

    def stop(self, *args, **kwargs):
        logger.info('stopping Loafer ...')
        if callable(self._on_stop_callback):
            self._on_stop_callback()

        logger.info('cancel schedulled operations ...')
        for task in asyncio.Task.all_tasks(self.loop):
            task.cancel()
            if task.cancelled() or task.done():
                continue

            with suppress(CancelledError):
                self.loop.run_until_complete(task)

        self._executor.shutdown(wait=True)
