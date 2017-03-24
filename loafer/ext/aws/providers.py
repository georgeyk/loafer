import asyncio
import logging

import aiobotocore
import botocore.exceptions
from cached_property import cached_property

from loafer.exceptions import ProviderError

logger = logging.getLogger(__name__)


class SQSProvider:
    def __init__(self, source, endpoint_url=None, use_ssl=True, options=None, loop=None):
        self.source = source
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl
        self._loop = loop or asyncio.get_event_loop()
        self._options = options or {}
        self._queue_url = None

    @cached_property
    def client(self):
        session = aiobotocore.get_session(loop=self._loop)
        return session.create_client('sqs', endpoint_url=self.endpoint_url, use_ssl=self.use_ssl)

    async def get_queue_url(self):
        if not self._queue_url:
            response = await self.client.get_queue_url(QueueName=self.source)
            self._queue_url = response['QueueUrl']
        return self._queue_url

    async def confirm_message(self, message):
        logger.info('confirm message (ACK/deletion)')

        receipt = message['ReceiptHandle']
        logger.debug('receipt={!r}'.format(receipt))

        queue_url = await self.get_queue_url()
        return await self.client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)

    async def fetch_messages(self):
        queue_url = await self.get_queue_url()
        logger.debug('fetching messages on {}'.format(queue_url))

        try:
            response = await self.client.receive_message(QueueUrl=queue_url, **self._options)
        except botocore.exceptions.ClientError as exc:
            raise ProviderError('Error when fetching messages') from exc

        return response.get('Messages', [])

    def stop(self):
        self.client.close()
