import asyncio
import logging

from loafer.exceptions import DeleteMessage, KeepMessage

logger = logging.getLogger(__name__)


# Job examples
# Jobs are the units where the messages are sent as parameters


# The regular function will be executed in the threadpool
def example_job(*args, **kwargs):
    message = 'Called example_job with args={} kwargs={}'.format(args, kwargs)
    logger.warning(message)


# The coroutine will be scheduled in the event loop
async def async_example_job(*args, **kwargs):
    message = 'Called async_example_job with args={} kwargs={}'.format(args, kwargs)
    logger.warning(message)


async def reject_message_job(*args, **kwargs):
    raise DeleteMessage()


async def ignore_message_job(*args, **kwargs):
    raise KeepMessage()


async def random_int_job(number):
    logger.info('Handling: {}'.format(number))
    # mimic i/o  operation
    await asyncio.sleep(0.5)
