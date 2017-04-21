import logging

import botocore.exceptions

from loafer.exceptions import ProviderError
from loafer.providers import AbstractProvider
from .bases import BaseSQSClient

logger = logging.getLogger(__name__)


class SQSProvider(AbstractProvider, BaseSQSClient):

    def __init__(self, queue_name, options=None, **kwargs):
        self.queue_name = queue_name
        self._options = options or {}
        super().__init__(**kwargs)

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.queue_name)

    async def confirm_message(self, message):
        logger.info('confirm message (ack/deletion)')

        receipt = message['ReceiptHandle']
        logger.debug('receipt={!r}'.format(receipt))

        queue_url = await self.get_queue_url(self.queue_name)
        return await self.client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)

    async def fetch_messages(self):
        logger.debug('fetching messages on {}'.format(self.queue_name))
        try:
            queue_url = await self.get_queue_url(self.queue_name)
            response = await self.client.receive_message(QueueUrl=queue_url, **self._options)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as exc:
            raise ProviderError('error fetching messages') from exc

        return response.get('Messages', [])

    def stop(self):
        logger.info('stopping {}'.format(self))
        self.client.close()
