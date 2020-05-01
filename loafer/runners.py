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

    def start(self, debug=False):
        if debug:
            self.loop.set_debug(enabled=debug)

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

    def _cancel_all_tasks(self):
        to_cancel = asyncio.Task.all_tasks(self.loop)
        if not to_cancel:
            return
        for task in to_cancel:
            task.cancel()

        self.loop.run_until_complete(
            asyncio.gather(*to_cancel, loop=self.loop, return_exceptions=True)
        )
        for task in to_cancel:
            if task.cancelled():
                continue
            if task.exception() is not None:
                self.loop.call_exception_handler({
                    'message': 'unhandled exception during asyncio.run() shutdown',
                    'exception': task.exception(),
                    'task': task,
                })

    def stop(self, *args, **kwargs):
        logger.info('stopping Loafer ...')
        if callable(self._on_stop_callback):
            self._on_stop_callback()

        logger.info('cancel schedulled operations ...')
        with suppress(CancelledError):
            self._cancel_all_tasks()

        self._executor.shutdown(wait=True)
