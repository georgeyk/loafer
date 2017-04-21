import asyncio
import logging

from cached_property import cached_property

from .dispatchers import LoaferDispatcher
from .exceptions import ConfigurationError
from .routes import Route
from .runners import LoaferRunner

logger = logging.getLogger(__name__)


class LoaferManager:
    def __init__(self, routes, runner=None):
        self.runner = runner or LoaferRunner(on_stop_callback=self.on_loop__stop)
        self.routes = routes

    @cached_property
    def dispatcher(self):
        if not (self.routes and all(isinstance(r, Route) for r in self.routes)):
            raise ConfigurationError('invalid routes to dispatch, routes={}'.format(self.routes))

        return LoaferDispatcher(self.routes)

    def run(self, forever=True):
        loop = self.runner.loop
        self._future = asyncio.gather(
            self.dispatcher.dispatch_providers(loop, forever=forever),
            loop=loop,
        )
        self._future.add_done_callback(self.on_future__errors)
        self.runner.start(self._future, run_forever=forever)

    #
    # Callbacks
    #

    def on_future__errors(self, future):
        exc = future.exception()
        # Unhandled errors crashes the event loop execution
        if isinstance(exc, BaseException):
            logger.critical('fatal error caught: {!r}'.format(exc))
            self.runner.stop()

    def on_loop__stop(self, *args, **kwargs):
        logger.info('cancel schedulled operations ...')
        for task in asyncio.Task.all_tasks(self.runner.loop):
            logger.debug('cancelling {}'.format(task))
            task.cancel()

        if hasattr(self, '_future'):
            self._future.cancel()

        self.dispatcher.stop()
