import asyncio

# https://github.com/getsentry/raven-aiohttp


async def sentry_handler(client, loop=None):
    loop = loop or asyncio.get_event_loop()

    def send_to_sentry(job, *exc_info):
        client.captureException(
            exc_info=exc_info,
            extra={
                'job_id': job.id,
                'func': job.func_name,
                'args': job.args,
                'kwargs': job.kwargs,
                'description': job.description,
            }
        )
