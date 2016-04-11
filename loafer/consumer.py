# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import json
from functools import partial
import logging

import boto3
import botocore.exceptions

from .conf import settings
from .exceptions import ConsumerError

logger = logging.getLogger(__name__)


class AsyncSQSConsumer(object):

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._semaphore = asyncio.Semaphore(settings.MAX_JOBS)
        self._client = boto3.client('sqs')

    async def process_message(self, route, message):
        logger.info('Message received, handling to route={}'.format(route))
        logger.debug('Processing Message={}', message)

        # TODO: better heuristic
        try:
            body = json.loads(message['Body'])
        except json.decoder.JSONDecodeError:
            body = message['Body']

        content = body
        if isinstance(body, dict):
            if 'Message' in body:
                content = body['Message']

        # Since we don't know what will happen on message handler, use semaphore
        # to protect scheduling or executing too many coroutines/threads
        with await self._semaphore:
            # TODO: depending on content type, we should pass as *args or **kwargs
            logger.info('Message content data type is {!r}'.format(type(content)))
            await route.handle_message(content)

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
                try:
                    messages = await router.fetch_messages()
                except botocore.exceptions.ClientError as exc:
                    logger.exception(exc)
                    raise ConsumerError('Error when fetching messages') from exc

                for message in messages:
                    await self.process_message(router, message)
