import json
import logging

from loafer.message_translators import AbstractMessageTranslator

logger = logging.getLogger(__name__)


class SQSMessageTranslator(AbstractMessageTranslator):

    def translate(self, message):
        translated = {'content': None, 'metadata': {}}
        try:
            body = message['Body']
        except (KeyError, TypeError):
            logger.error('missing Body key in SQS message. It really came from SQS ?'
                         '\nmessage={!r}'.format(message))
            return translated

        try:
            translated['content'] = json.loads(body)
        except json.decoder.JSONDecodeError as exc:
            logger.error('error={!r}, message={!r}'.format(exc, message))
            return translated

        message.pop('Body')
        translated['metadata'].update(message)
        return translated


class SNSMessageTranslator(AbstractMessageTranslator):

    def translate(self, message):
        translated = {'content': None, 'metadata': {}}
        try:
            body = json.loads(message['Body'])
            message_body = body.pop('Message')
        except (KeyError, TypeError):
            logger.error(
                'Missing Body or Message key in SQS message. It really came from SNS ?'
                '\nmessage={!r}'.format(message))
            return translated

        translated['metadata'].update(message)
        translated['metadata'].pop('Body')

        try:
            translated['content'] = json.loads(message_body)
        except (json.decoder.JSONDecodeError, TypeError) as exc:
            logger.error('error={!r}, message={!r}'.format(exc, message))
            return translated

        translated['metadata'].update(body)
        return translated
