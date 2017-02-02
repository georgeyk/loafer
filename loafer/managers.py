import asyncio
import logging

from cached_property import cached_property

from .dispatcher import LoaferDispatcher
from .runners import LoaferRunner

logger = logging.getLogger(__name__)


class LoaferManager:
    def __init__(self, routes, runner=None):
        self.runner = runner or LoaferRunner(on_stop_callback=self.on_loop__stop)
        self.routes = routes

    @cached_property
    def dispatcher(self):
        # TODO: check routes
        return LoaferDispatcher(self.routes)

    def run(self, forever=True):
        self._future = asyncio.gather(self.dispatcher.dispatch_providers(), loop=self.runner.loop)
        self._future.add_done_callback(self.on_future__errors)
        self.runner.start(self._future, run_forever=forever)

    #
    # Callbacks
    #

    def on_future__errors(self, future):
        exc = future.exception()
        # Unhandled errors crashes the event loop execution
        if isinstance(exc, BaseException):
            logger.critical('Fatal error caught: {!r}'.format(exc))
            self.runner.stop()

    def on_loop__stop(self, *args, **kwargs):
        logger.debug('Stopping consumers ...')
        self.dispatcher.stop_providers()

        if hasattr(self, '_future'):
            logger.debug('Cancel schedulled operations ...')
            self._future.cancel()
