import json

import boto3


def sqs_publish(queue, message):
    _client = boto3.client('sqs')

    if queue.startswith('https://'):
        queue_url = queue
    else:
        response = _client.get_queue_url(QueueName=queue)
        queue_url = response['QueueUrl']

    return _client.send_message(QueueUrl=queue_url, MessageBody=message)


def sns_publish(topic, message):
    _client = boto3.client('sns')
    if topic.startswith('arn:'):
        arn = topic
    else:
        topics = _client.list_topics()
        for topic_data in topics['Topics']:
            if topic_data['TopicArn'].endswith(topic):
                arn = topic_data['TopicArn']
                break

    msg = json.dumps({'default': message})
    return _client.publish(TopicArn=arn, MessageStructure='json', Message=msg)
