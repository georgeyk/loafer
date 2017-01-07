import asyncio
import logging

from cached_property import cached_property

from .dispatcher import LoaferDispatcher
from .runners import LoaferRunner

logger = logging.getLogger(__name__)


class LoaferManager:

    def __init__(self, routes, consumers, runner=None):
        self.runner = runner or LoaferRunner(on_stop_callback=self.on_loop__stop)
        self.routes = routes
        self.consumers = consumers

    @cached_property
    def dispatcher(self):
        return LoaferDispatcher(self.routes, self.consumers)

    def run(self, forever=True):
        self._future = asyncio.gather(self.dispatcher.dispatch_providers())
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
