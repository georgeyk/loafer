import logging

logger = logging.getLogger(__name__)


class StringMessageTranslator:

    def translate(self, message):
        logger.debug('{} will translate {}'.format(type(self).__name__, message))
        return {'content': str(message)}
