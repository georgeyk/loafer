# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import json
from functools import partial
import logging

import boto3

from .conf import settings

logger = logging.getLogger(__name__)


class AsyncSQSConsumer(object):

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._semaphore = asyncio.Semaphore(settings.MAX_JOBS)
        self._client = boto3.client('sqs')

    async def process_message(self, route, message):
        logger.info('Message received, handling to route={}'.format(route))
        logger.debug('Processing Message={}', message)

        body = json.loads(message['Body'])
        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            # long running process
            await route.handle_message(body['Message'])

        await self.ack_message(route.queue_url, message['ReceiptHandle'])

    async def ack_message(self, queue, receipt):
        logger.info('Acking message')
        logger.debug('receipt={}'.format(receipt))

        fn = partial(self._client.delete_message, QueueUrl=queue, ReceiptHandle=receipt)
        # XXX: Refactor this when boto support asyncio
        return await self._loop.run_in_executor(None, fn)

    async def consume(self, routes):
        while True:
            for router in routes:
                messages = await router.fetch_messages()
                for message in messages:
                    await self.process_message(router, message)
