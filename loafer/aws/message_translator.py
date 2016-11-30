import json
import logging

logger = logging.getLogger(__name__)


class SQSMessageTranslator:

    def translate(self, message):
        try:
            body = message['Body']
        except (KeyError, TypeError):
            logger.error('missing Body key in SQS message. It really came from SQS ?'
                         '\nmessage={}'.format(message))
            return {'content': None}

        try:
            return {'content': json.loads(body)}
        except json.decoder.JSONDecodeError as exc:
            logger.error('error={!r} message={}'.format(exc, message))
            return {'content': None}


class SNSMessageTranslator:
    def translate(self, message):
        try:
            body = json.loads(message['Body'])
            message = body['Message']
        except (KeyError, TypeError):
            logger.error(
                'Missing Body or Message key in SQS message. It really came from SNS ?'
                '\nmessage={}'.format(message))
            return {'content': None}

        try:
            return {'content': json.loads(message)}
        except (json.decoder.JSONDecodeError, TypeError) as exc:
            logger.error('error={!r} message={}'.format(exc, message))
            return {'content': None}
