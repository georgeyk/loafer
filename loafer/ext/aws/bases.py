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

    async def get_queue_url(self, queue_name):
        if queue_name not in self._cached_queue_urls:
            response = await self.client.get_queue_url(QueueName=queue_name)
            self._cached_queue_urls[queue_name] = response['QueueUrl']

        return self._cached_queue_urls[queue_name]


class BaseSNSClient:
    def __init__(self, endpoint_url=None, use_ssl=True, loop=None):
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl
        self._loop = loop or asyncio.get_event_loop()
        self._cached_topic_arns = {}

    @cached_property
    def client(self):
        session = aiobotocore.get_session(loop=self._loop)
        return session.create_client('sns', endpoint_url=self.endpoint_url, use_ssl=self.use_ssl)

    async def get_topic_arn(self, topic_name):
        if topic_name not in self._cached_topic_arns:
            topics = await self.client.list_topics()
            for topic_data in topics['Topics']:
                arn = topic_data['TopicArn']
                name = arn.split(':')[-1]
                self._cached_topic_arns[name] = arn

        return self._cached_topic_arns[topic_name]
