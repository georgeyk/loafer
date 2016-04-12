# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
from functools import partial
import logging

import boto3
import botocore.exceptions

from ..conf import settings
from ..exceptions import ConsumerError

logger = logging.getLogger(__name__)


class Consumer(object):

    def __init__(self, source_name, loop=None):
        self._source_name = source_name
        self._loop = loop or asyncio.get_event_loop()
        self._client = boto3.client('sqs')

    async def get_queue_url(self):
        fn = partial(self._client.get_queue_url, QueueName=self._source_name)
        # XXX: Refactor this when boto support asyncio
        response = await self._loop.run_in_executor(None, fn)
        return response['QueueUrl']

    async def confirm_message(self, receipt):
        logger.info('Confirming message (ACK)')
        logger.debug('receipt={}'.format(receipt))

        queue_url = await self.get_queue_url()
        fn = partial(self._client.delete_message, QueueUrl=queue_url, ReceiptHandle=receipt)
        # XXX: Refactor this when boto support asyncio
        return await self._loop.run_in_executor(None, fn)

    async def fetch_messages(self):
        queue_url = await self.get_queue_url()
        fn = partial(self._client.receive_message,
                     QueueUrl=queue_url,
                     WaitTimeSeconds=settings.SQS_WAIT_TIME_SECONDS,
                     MaxNumberOfMessages=settings.SQS_MAX_MESSAGES)
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
