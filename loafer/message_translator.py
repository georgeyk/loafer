# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

logger = logging.getLogger(__name__)


class StringMessageTranslator(object):

    def translate(self, message):
        logger.debug('{} will translate {}'.format(self.__class__.__name__, message))
        return {'content': str(message)}
