# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from functools import partial
import logging

import boto3
import botocore.exceptions

from ..exceptions import ConsumerError

logger = logging.getLogger(__name__)


class Consumer(object):

    def __init__(self, source, options=None, loop=None):
        self.source = source
        self._loop = loop or asyncio.get_event_loop()
        self._client = None
        self._consumer_options = options

    def get_client(self):
        if self._client is None:
            self._client = boto3.client('sqs')
        return self._client

    async def get_queue_url(self):
        fn = partial(self.get_client().get_queue_url, QueueName=self.source)
        # XXX: Refactor this when boto support asyncio
        response = await self._loop.run_in_executor(None, fn)
        return response['QueueUrl']

    async def confirm_message(self, message):
        logger.info('Confirm message (ACK/Deletion)')

        receipt = message['ReceiptHandle']
        logger.debug('receipt={}'.format(receipt))

        queue_url = await self.get_queue_url()
        fn = partial(self.get_client().delete_message, QueueUrl=queue_url, ReceiptHandle=receipt)
        # XXX: Refactor this when boto support asyncio
        return await self._loop.run_in_executor(None, fn)

    async def fetch_messages(self):
        queue_url = await self.get_queue_url()
        logger.info('Fetching messages on {}'.format(queue_url))

        options = self._consumer_options or {}
        fn = partial(self.get_client().receive_message, QueueUrl=queue_url, **options)
        # XXX: Refactor this when boto support asyncio
        response = await self._loop.run_in_executor(None, fn)
        return response.get('Messages', [])

    async def consume(self):
        try:
            messages = await self.fetch_messages()
        except botocore.exceptions.ClientError as exc:
            logger.exception(exc)
            raise ConsumerError('Error when fetching messages') from exc

        return messages
