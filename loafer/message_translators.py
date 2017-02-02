import logging

logger = logging.getLogger(__name__)


class StringMessageTranslator:

    def translate(self, message):
        logger.debug('{!r} will translate {}'.format(type(self).__name__, message))
        return {'content': str(message)}
