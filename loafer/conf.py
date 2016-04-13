# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from prettyconf import config


class Settings(object):
    LOAFER_LOGLEVEL = config('LOAFER_LOGLEVEL', default='WARNING')
    LOAFER_LOG_FORMAT = config('LOAFER_LOG_FORMAT',
                               default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    MAX_JOBS = config('MAX_JOBS', default=10)
    MAX_THREAD_POOL = config('MAX_THREAD_POOL', default=None)
    # SQS long-polling
    SQS_WAIT_TIME_SECONDS = config('SQS_WAIT_TIME_SECONDS', default=5)
    # 10 is the maximum value
    SQS_MAX_MESSAGES = config('SQS_MAX_MESSAGES', default=10)

    LOAFER_ROUTES = [('test-images', 'loafer.jobs.async_example_job')]

    LOAFER_DEFAULT_CONSUMER_CLASS = 'loafer.aws.consumer.Consumer'

    def __init__(self, **defaults):
        if defaults:
            safe_defaults = {k: v for k, v in defaults.items() if k.isupper()}
            self.__dict__.update(safe_defaults)


settings = Settings()
