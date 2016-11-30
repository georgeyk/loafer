# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging
import random


logger = logging.getLogger(__name__)


class RandomIntConsumer(object):

    def __init__(self, *args, **kwargs):
        # receive consumer options
        pass

    async def consume(self):
        number = random.randint(1, 1000)
        logger.info('Retrived number: {}'.format(number))
        return [number]

    async def confirm_message(self, message):
        logger.info('Confirmed: {}'.format(message))
        return True
