# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import json
from functools import partial
import logging

import boto3

from prettyconf import config

from .conf import settings

logger = logging.getLogger(__name__)


class AsyncSQSConsumer(object):
    def __init__(self):
        self._semaphore = asyncio.Semaphore(settings.MAX_JOBS)
        self._client = boto3.client('sqs')

        # XXX: Refactor this
        self._queue = config('QUEUE')

    async def _receive_messages(self, loop):
        fn = partial(self._client.receive_message, QueueUrl=self._queue, WaitTimeSeconds=5)
        # XXX: Refactor this when boto support asyncio
        response = await loop.run_in_executor(None, fn)
        return response.get('Messages', [])

    async def process_message(self, message, loop):
        body = json.loads(message['Body'])
        print(body['Message'])
        print(type(body))
        # long running process
        asyncio.sleep(5)
        return message['ReceiptHandle']

    async def ack_message(self, receipt, loop):
        fn = partial(self._client.delete_message, QueueUrl=self._queue, ReceiptHandle=receipt)
        # XXX: Refactor this when boto support asyncio
        return await loop.run_in_executor(None, fn)

    async def consume(self, loop):
        while True:
            messages = await self._receive_messages(loop)
            for message in messages:
                with await self._semaphore:
                    receipt = await self.process_message(message, loop)
                    await self.ack_message(receipt, loop)
