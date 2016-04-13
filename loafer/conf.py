# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from prettyconf import config


class Settings(object):
    # Logging
    LOAFER_LOGLEVEL = config('LOAFER_LOGLEVEL', default='WARNING')
    LOAFER_LOG_FORMAT = config('LOAFER_LOG_FORMAT',
                               default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Max concurrent jobs (asyncio)
    LOAFER_MAX_JOBS = config('LOAFER_MAX_JOBS', default=10)

    # Default value are determined from the number of machine cores
    LOAFER_MAX_THREAD_POOL = config('LOAFER_MAX_THREAD_POOL', default=None)

    # Consumer

    # Currently, only AWS is supported, references:
    # http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-long-polling.html
    # http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html
    # By default, SQS does not set long-polling (WaitTimeSeconds) and the MaxNumberOfMessages is 1
    # TODO: tweak default values for acceptable performance
    LOAFER_DEFAULT_CONSUMER_CLASS = 'loafer.aws.consumer.Consumer'
    LOAFER_DEFAULT_CONSUMER_OPTIONS = {'WaitTimeSeconds': 5,  # from 1-20
                                       'MaxNumberOfMessages': 5}  # from 1-10

    # Translator
    LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS = 'loafer.message_translator.StringMessageTranslator'

    # Routes
    LOAFER_ROUTES = [('test-images', 'loafer.jobs.async_example_job')]

    def __init__(self, **defaults):
        if defaults:
            safe_defaults = {k: v for k, v in defaults.items()
                             if k.isupper() and k.startswith('LOAFER_')}
            self.__dict__.update(safe_defaults)


settings = Settings()
