import asyncio
import logging

logger = logging.getLogger(__name__)


class Retry:
    def __init__(self, exceptions=Exception, tries=-1, delay=0):
        # TODO implement max delay and backoff
        assert tries, 'invalid tries count'

        self.exceptions = exceptions
        self._tries = tries
        self.max_tries = tries
        self.delay = delay

    async def deliver(self, route, raw_message):
        while self._tries:
            logger.debug('try #', self._tries)
            try:
                return await route._deliver(raw_message)
            except self.exceptions:
                self._tries -= 1
                if not self._tries:
                    self._tries = self.max_tries
                    logger.debug('out of tries')
                    raise

                await asyncio.sleep(self.delay)
