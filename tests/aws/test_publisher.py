# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from loafer.aws.publisher import sqs_publish


def test_sqs_publish(mock_boto_client_sqs):
    with mock_boto_client_sqs as mock_sqs:
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
