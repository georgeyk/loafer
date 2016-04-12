# -*- coding: utf-8 -*-

import asyncio
from functools import partial
import importlib
import logging

import boto3

from cached_property import cached_property

from .conf import settings


logger = logging.getLogger(__name__)


class Route(object):
    def __init__(self, queue, handler, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._client = boto3.client('sqs')

        self.queue_name = queue
        self._handler = handler

    def __str__(self):
        return '<Router(queue={} handler={})>'.format(self.queue_name, self._handler)

    @cached_property
    def queue_url(self):
        response = self._client.get_queue_url(QueueName=self.queue_name)
        return response['QueueUrl']

    @cached_property
    def handler(self):
        package = '.'.join(self._handler.split('.')[:-1])
        name = self._handler.split('.')[-1]
        module = importlib.import_module(package)
        return getattr(module, name)

    async def handle_message(self, message):
        if asyncio.iscoroutinefunction(self.handler):
            logger.info('Handler is coroutine! {!r}'.format(self.handler))
            return await self.handler(message)
        else:
            logger.info('Handler will run in a separate thread: {!r}'.format(self.handler))
            return await self._loop.run_in_executor(None, self.handler, message)

    async def fetch_messages(self):
        fn = partial(self._client.receive_message,
                     QueueUrl=self.queue_url,
                     WaitTimeSeconds=settings.SQS_WAIT_TIME_SECONDS,
                     MaxNumberOfMessages=settings.SQS_MAX_MESSAGES)
        response = await self._loop.run_in_executor(None, fn)
        return response.get('Messages', [])
