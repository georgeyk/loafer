# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

from prettyconf import config


config.starting_path = os.getcwd()


class Settings(object):
    # Logging
    LOAFER_LOGLEVEL = config('LOAFER_LOGLEVEL', default='WARNING')
    LOAFER_LOG_FORMAT = config('LOAFER_LOG_FORMAT',
                               default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Max concurrent jobs (asyncio)
    LOAFER_MAX_JOBS = config('LOAFER_MAX_JOBS', default=10)

    # Default value are determined from the number of machine cores
    LOAFER_MAX_THREAD_POOL = config('LOAFER_MAX_THREAD_POOL', default=None)

    # Translator
    LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS = config(
        'LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS',
        default='loafer.aws.message_translator.SQSMessageTranslator')

    # Routes
    LOAFER_ROUTES = [
        {'name': config('LOAFER_DEFAULT_ROUTE_NAME', default='default'),
         'source': config('LOAFER_DEFAULT_ROUTE_SOURCE'),
         'handler': config('LOAFER_DEFAULT_ROUTE_HANDLER',
                           default='loafer.example.jobs.async_example_job'),
         'message_translator': LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS},
    ]

    # Consumer

    # Currently, only AWS is supported, references:
    # http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-long-polling.html
    # http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html

    # By default, SQS does not set long-polling (WaitTimeSeconds) and the MaxNumberOfMessages is 1
    # TODO: tweak default values for acceptable performance
    LOAFER_DEFAULT_CONSUMER_CLASS = config('LOAFER_DEFAULT_CONSUMER_CLASS',
                                           default='loafer.aws.consumer.Consumer')
    LOAFER_DEFAULT_CONSUMER_OPTIONS = config(
        'LOAFER_DEFAULT_CONSUMER_OPTIONS',
        default={'WaitTimeSeconds': 5,  # from 1-20
                 'MaxNumberOfMessages': 5})  # from 1-10

    # Setting LOAFER_CONSUMERS is only needed when there's more than one consumer.
    # Otherwise, all routes will use the LOAFER_DEFAULT_CONSUMER_CLASS
    # and LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS automatically.
    # This is an example configuration that will be available in the future:
    LOAFER_CONSUMERS = [
        {'route_source': {'consumer_class': LOAFER_DEFAULT_CONSUMER_CLASS,
                          'consumer_options': LOAFER_DEFAULT_CONSUMER_OPTIONS}},
    ]

    def __init__(self, **defaults):
        if defaults:
            safe_defaults = {k: v for k, v in defaults.items()
                             if k.isupper() and k.startswith('LOAFER_')}
            self.__dict__.update(safe_defaults)


settings = Settings()
