# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

logger = logging.getLogger(__name__)

# Job examples
# Jobs are the units where the messages are sent as parameters


# The regular function will be executed in the threadpool
def example_job(*args, **kwargs):
    logger.info('Got message: example_job with  args={} kwargs={}'.format(args, kwargs))


# The coroutine will be scheduled in the event loop
async def async_example_job(*args, **kwargs):
    logger.info('Got message: async_example_job with args={} kwargs={}'.format(args, kwargs))
