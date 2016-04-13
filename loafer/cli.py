# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

import click

from . import __version__
from .conf import settings
from .manager import LoaferManager
from .aws.publisher import Publisher
from .utils import echo


logger = logging.getLogger(__name__)


def _bootstrap():
    logging.basicConfig(level=settings.LOAFER_LOGLEVEL,
                        format=settings.LOAFER_LOG_FORMAT)


def main():

    echo('Starting Loafer (Version={}) ...'.format(__version__),
         bold=True, fg='green')

    _bootstrap()

    echo('Hit CTRL-C to stop', bold=True, fg='yellow')

    loafer = LoaferManager()
    loafer.start()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if context.invoked_subcommand is None:
        main()


@cli.command()
@click.option('--queue', default=None, help='SQS queue name ou url')
@click.option('--topic', default=None, help='SNS topic name ou arn')
@click.option('--msg', help='Message to publish (assumes json format)')
def publish(queue, topic, msg):
    # TODO: check the "click" way to validate parameters
    if not (queue or topic):
        raise click.UsageError('--queue or --topic parameter are missing')
    if queue and topic:
        raise click.UsageError('Use --queue OR --topic, not both')

    publisher = Publisher()
    if queue:
        service = 'sqs'
        destination = queue
    if topic:
        service = 'sns'
        destination = topic

    response = publisher.publish(service, destination, msg)
    echo('Response: {}'.format(response))
