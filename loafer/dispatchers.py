import sys
import asyncio
import logging

from .exceptions import DeleteMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher:
    def __init__(self, routes, max_jobs=None):
        self.routes = routes
        jobs = max_jobs or len(routes) * 2
        self._semaphore = asyncio.Semaphore(jobs)

    async def dispatch_message(self, message, route):
        logger.debug('dispatching message to route={}'.format(route))
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
                exc_info = sys.exc_info()
                confirm_message = await route.error_handler(exc_info, message)

        return confirm_message

    async def process_route(self, route):
        provider = route.provider
        messages = await provider.fetch_messages()
        for message in messages:
            confirmation = await self.dispatch_message(message, route)
            if confirmation:
                await provider.confirm_message(message)

    async def _dispatch_tasks(self, loop):
        tasks = [self.process_route(route) for route in self.routes]
        done, _ = await asyncio.wait(tasks, loop=loop)
        # If any unhandled error happened, this will bring up the exception
        for task_done in done:
            task_done.result()

    async def dispatch_providers(self, loop, forever=True):
        if not forever:
            return await self._dispatch_tasks(loop)

        while True:
            await self._dispatch_tasks(loop)

    def stop(self):
        for route in self.routes:
            route.stop()
