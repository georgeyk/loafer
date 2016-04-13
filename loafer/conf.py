# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from prettyconf import config


class Settings(object):
    LOAFER_LOGLEVEL = config('LOAFER_LOGLEVEL', default='WARNING')
    LOAFER_LOG_FORMAT = config('LOAFER_LOG_FORMAT',
                               default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    LOAFER_MAX_JOBS = config('LOAFER_MAX_JOBS', default=10)
    LOAFER_MAX_THREAD_POOL = config('LOAFER_MAX_THREAD_POOL', default=None)
    # SQS long-polling
    LOAFER_SQS_WAIT_TIME_SECONDS = config('LOAFER_SQS_WAIT_TIME_SECONDS', default=5)
    # 10 is the maximum value
    LOAFER_SQS_MAX_MESSAGES = config('LOAFER_SQS_MAX_MESSAGES', default=10)

    LOAFER_ROUTES = [('test-images', 'loafer.jobs.async_example_job')]

    LOAFER_DEFAULT_CONSUMER_CLASS = 'loafer.aws.consumer.Consumer'

    def __init__(self, **defaults):
        if defaults:
            safe_defaults = {k: v for k, v in defaults.items()
                             if k.isupper() and k.startswith('LOAFER_')}
            self.__dict__.update(safe_defaults)


settings = Settings()
