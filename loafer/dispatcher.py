import asyncio
import logging

from .exceptions import RejectMessage, IgnoreMessage, DeleteMessage

logger = logging.getLogger(__name__)


class LoaferDispatcher:

    def __init__(self, routes, providers=None, max_jobs=None):
        self.routes = routes
        self.providers = providers or []
        jobs = max_jobs or len(routes) * 2
        self._semaphore = asyncio.Semaphore(jobs)
        self._stop_providers = True

    def get_provider(self, route):
        for provider in self.providers:
            if provider.source == route.source:
                return provider

        # TODO: refactor code, so this is not possible.
        logger.error('Provider not found for route={}'.format(route))
        raise ValueError('Provider not found for route={}'.format(route))

    def _translate_message(self, message, route):
        if not route.message_translator:
            logger.debug('route={} without message_translator set'.format(route))
            return message

        # in the future, we may change the route depending on message content
        try:
            content = route.message_translator.translate(message)['content']
        except Exception as exc:
            logger.error('error translating message content: {!r}'.format(exc))
            return None

        return content

    async def dispatch_message(self, message, route):
        logger.info('dispatching message to route={}'.format(route))

        content = self._translate_message(message, route)
        if content is None:
            logger.warning('message will be ignored:\n{}\n'.format(message))
            return False

        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            try:
                await route.deliver(content)
            except (DeleteMessage, RejectMessage) as exc:
                logger.info('explicit message rejection:\n{}\n'.format(message))
                # eg, we will return True at the end
            except IgnoreMessage as exc:
                logger.info('explicit message ignore:\n{}\n'.format(message))
                return False
            except asyncio.CancelledError as exc:
                msg = '"{}" was cancelled, the message will be ignored:\n{}\n'
                logger.warning(msg.format(route.handler_name, message))
                return False
            except Exception as exc:
                return await route.error_handler(type(exc), exc, message)

        return True

    async def dispatch_providers(self, sentinel=None):
        if sentinel is None or not callable(sentinel):
            self._stop_providers = False
            stopper = self._default_sentinel
        else:
            stopper = sentinel

        while not stopper():
            for route in self.routes:
                provider = self.get_provider(route)
                if not provider:
                    continue

                messages = await provider.fetch_messages()
                for message in messages:
                    confirmation = await self.dispatch_message(message, route)
                    if confirmation:
                        await provider.confirm_message(message)

    def _default_sentinel(self):
        return self._stop_providers

    def stop_providers(self):
        logger.info('Stopping providers')
        self._stop_providers = True
