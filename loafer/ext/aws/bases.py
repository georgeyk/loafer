import asyncio
import logging

import aiobotocore
from cached_property import cached_property

logger = logging.getLogger(__name__)


class BaseSQSClient:

    def __init__(self, endpoint_url=None, use_ssl=True, loop=None):
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl
        self._loop = loop or asyncio.get_event_loop()
        self._cached_queue_urls = {}

    @cached_property
    def client(self):
        session = aiobotocore.get_session(loop=self._loop)
        return session.create_client('sqs', endpoint_url=self.endpoint_url, use_ssl=self.use_ssl)

    async def get_queue_url(self, queue):
        if queue and (queue.startswith('http://') or queue.startswith('https://')):
            name = queue.split('/')[-1]
            self._cached_queue_urls[name] = queue
            queue = name

        if queue not in self._cached_queue_urls:
            response = await self.client.get_queue_url(QueueName=queue)
            self._cached_queue_urls[queue] = response['QueueUrl']

        return self._cached_queue_urls[queue]

    def stop(self):
        logger.info('closing client={}'.format(self.client))
        self.client.close()


class BaseSNSClient:

    def __init__(self, endpoint_url=None, use_ssl=True, loop=None):
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl
        self._loop = loop or asyncio.get_event_loop()

    @cached_property
    def client(self):
        session = aiobotocore.get_session(loop=self._loop)
        return session.create_client('sns', endpoint_url=self.endpoint_url, use_ssl=self.use_ssl)

    async def get_topic_arn(self, topic):
        arn_prefix = 'arn:aws:sns:'
        if topic.startswith(arn_prefix):
            return topic
        return '{}*:{}'.format(arn_prefix, topic)

    def stop(self):
        logger.info('closing client={}'.format(self.client))
        self.client.close()
