import asyncio
import logging

import botocore.exceptions

from .bases import BaseSQSClient
from loafer.exceptions import ProviderError
from loafer.providers import AbstractProvider

logger = logging.getLogger(__name__)


class SQSProvider(AbstractProvider, BaseSQSClient):

    def __init__(self, queue_name, options=None, **kwargs):
        self.queue_name = queue_name
        self._options = options or {}
        super().__init__(**kwargs)

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.queue_name)

    async def confirm_message(self, message):
        receipt = message['ReceiptHandle']
        logger.info('confirm message (ack/deletion), receipt={!r}'.format(receipt))

        queue_url = await self.get_queue_url(self.queue_name)
        try:
            async with self.get_client() as client:
                return await client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
        except botocore.exceptions.ClientError as exc:
            if exc.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                return True

            raise

    async def fetch_messages(self):
        logger.debug('fetching messages on {}'.format(self.queue_name))
        try:
            queue_url = await self.get_queue_url(self.queue_name)
            async with self.get_client() as client:
                response = await client.receive_message(QueueUrl=queue_url, **self._options)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as exc:
            raise ProviderError('error fetching messages from queue={}: {}'.format(self.queue_name, str(exc))) from exc

        return response.get('Messages', [])

    async def _client_stop(self):
        async with self.get_client() as client:
            await client.close()

    def stop(self):
        logger.info('stopping {}'.format(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._client_stop())
        return super().stop()
