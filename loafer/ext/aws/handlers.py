import json
import logging

from .bases import BaseSQSClient, BaseSNSClient

logger = logging.getLogger(__name__)


class SQSHandler(BaseSQSClient):
    queue_name = None

    def __init__(self, queue_name=None, **kwargs):
        self.queue_name = queue_name or self.queue_name
        super().__init__(**kwargs)

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.queue_name)

    async def publish(self, message, encoder=json.dumps):
        if not self.queue_name:
            raise ValueError('{}: missing queue_name attribute'.format(type(self).__name__))

        if encoder:
            message = encoder(message)

        logger.debug('publishing, queue={}, message={}'.format(self.queue_name, message))

        queue_url = await self.get_queue_url(self.queue_name)
        return await self.client.send_message(QueueUrl=queue_url, MessageBody=message)

    async def handle(self, message, *args):
        return await self.publish(message)


class SNSHandler(BaseSNSClient):
    topic_name = None

    def __init__(self, topic_name=None, **kwargs):
        self.topic_name = topic_name or self.topic_name
        super().__init__(**kwargs)

    def __str__(self):
        return '<{}: {}>'.format(type(self).__name__, self.topic_name)

    async def publish(self, message, encoder=json.dumps):
        if not self.topic_name:
            raise ValueError('{}: missing topic_name attribute'.format(type(self).__name__))

        if encoder:
            message = encoder(message)

        logger.debug('publishing, topic={}, message={}'.format(self.topic_name, message))

        msg = json.dumps({'default': message})
        topic_arn = await self.get_topic_arn(self.topic_name)
        return await self.client.publish(TopicArn=topic_arn, MessageStructure='json', Message=msg)

    async def handle(self, message, *args):
        return await self.publish(message)
