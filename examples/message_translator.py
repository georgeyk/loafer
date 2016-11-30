# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

logger = logging.getLogger(__name__)


class IntMessageTranslator(object):

    def translate(self, message):
        logger.info('Translating: {}'.format(message))
        try:
            content = int(message)
        except ValueError:
            content = None

        return {'content': content}
