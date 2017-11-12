import asyncio
import logging
import sys

from .exceptions import DeleteMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher:

    def __init__(self, routes, max_jobs=None):
        self.routes = routes
        jobs = max_jobs or len(routes) * 10
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
                logger.info('explicit message deletion\n{}\n'.format(message))
                confirm_message = True
            except asyncio.CancelledError as exc:
                msg = '"{!r}" was cancelled, the message will not be acknowledged:\n{}\n'
                logger.warning(msg.format(route.handler, message))
            except Exception as exc:
                logger.exception('{!r}'.format(exc))
                exc_info = sys.exc_info()
                confirm_message = await route.error_handler(exc_info, message)

        return confirm_message

    async def _process_message(self, message, route):
        confirmation = await self.dispatch_message(message, route)
        if confirmation:
            provider = route.provider
            await provider.confirm_message(message)
        return confirmation

    async def _get_route_messages(self, route):
        if route.enabled:
            messages = await route.provider.fetch_messages()
        else:
            messages = []
        return {'route': route, 'messages': messages}

    async def _get_routes_messages(self, loop):
        tasks = []

        for route in self.routes:
            task = self._get_route_messages(route)
            tasks.append(task)

        done, _ = await asyncio.wait(tasks, loop=loop)
        return [t.result() for t in done]

    async def _dispatch_tasks(self, loop):
        tasks = []

        routes_messages = await self._get_routes_messages(loop)
        for route_messages in routes_messages:
            route = route_messages['route']
            messages = route_messages['messages']
            for message in messages:
                task = self._process_message(message, route)
                tasks.append(task)

        if not tasks:
            return []

        done, _ = await asyncio.wait(tasks, loop=loop)
        # If any unhandled error happened, this will bring up the exception
        return [t.result() for t in done]

    async def dispatch_providers(self, loop, forever=True):
        if not forever:
            return await self._dispatch_tasks(loop)

        while True:
            await self._dispatch_tasks(loop)

    def stop(self):
        for route in self.routes:
            route.stop()
