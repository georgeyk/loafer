import asyncio
import logging

from .exceptions import DeleteMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher:
    def __init__(self, routes, max_jobs=None):
        self.routes = routes
        jobs = max_jobs or len(routes) * 2
        self._semaphore = asyncio.Semaphore(jobs)
        self._stop_providers = True

    async def dispatch_message(self, message, route):
        logger.info('dispatching message to route={!r}'.format(route))
        confirm_message = False
        if not message:
            logger.warning('message will be ignored:\n{!r}\n'.format(message))
            return confirm_message

        with await self._semaphore:
            try:
                confirm_message = await route.deliver(message)
            except DeleteMessage as exc:
                logger.info('explicit message deletion\n{!r}\n'.format(message))
                confirm_message = True
            except asyncio.CancelledError as exc:
                msg = '"{!r}" was cancelled, the message will not be acknowledged:\n{!r}\n'
                logger.warning(msg.format(route.handler, message))
            except Exception as exc:
                logger.exception('{!r}'.format(exc))
                confirm_message = await route.error_handler(type(exc), exc, message)

        return confirm_message

    async def process_route(self, route):
        provider = route.provider
        messages = await provider.fetch_messages()
        for message in messages:
            confirmation = await self.dispatch_message(message, route)
            if confirmation:
                await provider.confirm_message(message)

    async def dispatch_providers(self, sentinel=None):
        if sentinel is None or not callable(sentinel):
            self._stop_providers = False
            stopper = self._default_sentinel
        else:
            stopper = sentinel

        while not stopper():
            tasks = [self._loop.create_task(self.process_route(route))
                     for route in self.routes]
            await asyncio.wait(tasks, loop=self._loop)

    def _default_sentinel(self):
        return self._stop_providers

    def stop_providers(self):
        logger.info('Stopping providers')
        for route in self.routes:
            route.provider.stop()
        self._stop_providers = True
