import json

from loafer.ext.aws.publisher import sqs_publish, sns_publish


def test_sqs_publish(mock_boto_sync_client_sqs):
    with mock_boto_sync_client_sqs as mock_sqs:
        message = '{"test": "hey"}'
        response = sqs_publish('queue-name', message)
        assert response
        assert mock_sqs.called

        client = mock_sqs()
        assert client.send_message.called
        queue_url = client.get_queue_url()['QueueUrl']
        assert client.send_message.called_once_with(
            MessageBody='{}'.format(message),
            QueueUrl=queue_url)


def test_sqs_publish_with_queue_url(mock_boto_sync_client_sqs):
    with mock_boto_sync_client_sqs as mock_sqs:
        message = '{"test": "hey"}'
        response = sqs_publish('https://blabla/queue-name', message)
        assert response
        assert mock_sqs.called

        client = mock_sqs()
        assert client.send_message.called
        queue_url = client.get_queue_url()['QueueUrl']
        assert client.send_message.called_once_with(
            MessageBody='{}'.format(message),
            QueueUrl=queue_url)


def test_sns_publisher(mock_boto_sync_client_sns):
    with mock_boto_sync_client_sns as mock_sns:
        message = '{"test": "hey"}'
        topic = 'arn:blabla:topic-name'
        response = sns_publish(topic, message)
        assert response
        assert mock_sns.called

        client = mock_sns()
        assert client.publish.called
        message_sent = json.dumps({'default': message})
        assert client.publish.called_once_with(
            TopicArn=topic,
            MessageStructure='json',
            Message=message_sent)


def test_sns_publisher_with_topic_name(mock_boto_sync_client_sns):
    with mock_boto_sync_client_sns as mock_sns:
        message = '{"test": "hey"}'
        topic = 'topic-name'
        response = sns_publish(topic, message)
        assert response
        assert mock_sns.called

        client = mock_sns()
        assert client.publish.called
