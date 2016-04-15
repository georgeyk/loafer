# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

from ..exceptions import RejectMessage, IgnoreMessage

logger = logging.getLogger(__name__)


# Job examples
# Jobs are the units where the messages are sent as parameters


# The regular function will be executed in the threadpool
def example_job(*args, **kwargs):
    message = 'Called example_job with args={} kwargs={}'.format(args, kwargs)
    logger.warning(message)
    msg2 = 'args type is {} kwargs type is'.format(type(args), type(kwargs))
    logger.warning(msg2)


# The coroutine will be scheduled in the event loop
async def async_example_job(*args, **kwargs):
    message = 'Called async_example_job with args={} kwargs={}'.format(args, kwargs)
    logger.warning(message)
    msg2 = 'args type is {} kwargs type is'.format(type(args), type(kwargs))
    logger.warning(msg2)


async def reject_message_job(*args, **kwargs):
    raise RejectMessage()


async def ignore_message_job(*args, **kwargs):
    raise IgnoreMessage()
