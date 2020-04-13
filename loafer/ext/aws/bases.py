import logging

import aiobotocore

logger = logging.getLogger(__name__)


class _BotoClient:
    boto_service_name = None

    def __init__(self, **client_options):
        self._client_options = {
            'api_version': client_options.get('api_version', None),
            'aws_access_key_id': client_options.get('aws_access_key_id', None),
            'aws_secret_access_key': client_options.get('aws_secret_access_key', None),
            'aws_session_token': client_options.get('aws_session_token', None),
            'endpoint_url': client_options.get('endpoint_url', None),
            'region_name': client_options.get('region_name', None),
            'use_ssl': client_options.get('use_ssl', True),
            'verify': client_options.get('verify', None),
        }

    def get_client(self):
        session = aiobotocore.get_session()
        return session.create_client(self.boto_service_name, **self._client_options)

    async def stop(self):
        async with self.get_client() as client:
            logger.info('closing client{}'.format(client))
            await client.close()


class BaseSQSClient(_BotoClient):
    boto_service_name = 'sqs'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_queue_urls = {}

    async def get_queue_url(self, queue):
        if queue and (queue.startswith('http://') or queue.startswith('https://')):
            name = queue.split('/')[-1]
            self._cached_queue_urls[name] = queue
            queue = name

        if queue not in self._cached_queue_urls:
            async with self.get_client() as client:
                response = await client.get_queue_url(QueueName=queue)
                self._cached_queue_urls[queue] = response['QueueUrl']

        return self._cached_queue_urls[queue]


class BaseSNSClient(_BotoClient):
    boto_service_name = 'sns'

    async def get_topic_arn(self, topic):
        arn_prefix = 'arn:aws:sns:'
        if topic.startswith(arn_prefix):
            return topic
        return '{}*:{}'.format(arn_prefix, topic)
