import json

from .bases import BaseSQSClient, BaseSNSClient


class SQSHandler(BaseSQSClient):
    queue_name = None

    def __init__(self, queue_name=None, **kwargs):
        self.queue_name = queue_name or self.queue_name
        super().__init__(**kwargs)

    async def publish(self, message):
        if not self.queue_name:
            raise ValueError('{}: missing queue_name attribute'.format(type(self).__name__))

        queue_url = await self.get_queue_url(self.queue_name)
        return await self.client.send_message(QueueUrl=queue_url, MessageBody=message)

    async def handle(self, message, *args):
        return await self.publish(message)


class SNSHandler(BaseSNSClient):
    topic_name = None

    def __init__(self, topic_name=None, **kwargs):
        self.topic_name = topic_name or self.topic_name
        super().__init__(**kwargs)

    async def publish(self, message):
        if not self.topic_name:
            raise ValueError('{}: missing topic_name attribute'.format(type(self).__name__))

        topic_arn = await self.get_topic_arn(self.topic_name)
        msg = json.dumps({'default': message})
        return await self.client.publish(TopicArn=topic_arn, MessageStructure='json', Message=msg)

    async def handle(self, message, *args):
        return await self.publish(message)
