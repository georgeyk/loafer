import asyncio
import logging

from .exceptions import KeepMessage, DeleteMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher:

    def __init__(self, routes, max_jobs=None):
        self.routes = routes
        jobs = max_jobs or len(routes) * 2
        self._semaphore = asyncio.Semaphore(jobs)
        self._stop_providers = True

    def _translate_message(self, message, route):
        if not route.message_translator:
            logger.debug('route={!r} without message_translator set'.format(route))
            return message

        # in the future, we may change the route depending on message content
        try:
            content = route.message_translator.translate(message)['content']
        except Exception as exc:
            logger.error('error translating message content: {!r}'.format(exc))
            return None

        return content

    async def dispatch_message(self, message, route):
        logger.info('dispatching message to route={!r}'.format(route))

        content = self._translate_message(message, route)
        if content is None:
            logger.warning('message will be ignored:\n{!r}\n'.format(message))
            return False

        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            try:
                await route.deliver(content)
            except (DeleteMessage) as exc:
                logger.info('message acknowledged:\n{!r}\n'.format(message))
                # eg, we will return True at the end
            except KeepMessage as exc:
                logger.info('message not acknowledged:\n{!r}\n'.format(message))
                return False
            except asyncio.CancelledError as exc:
                msg = '"{}" was cancelled, the message will not be acknowledged:\n{!r}\n'
                logger.warning(msg.format(route.handler_name, message))
                return False
            except Exception as exc:
                return await route.error_handler(type(exc), exc, message)

        return True

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
        self._stop_providers = True
