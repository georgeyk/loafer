# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

import click

from . import __version__
from .conf import Settings, settings
from .manager import LoaferManager
from .aws.publisher import Publisher


logger = logging.getLogger(__name__)


def _bootstrap(custom_settings=None):
    configuration = custom_settings or settings
    logging.basicConfig(level=configuration.LOAFER_LOGLEVEL,
                        format=configuration.LOAFER_LOG_FORMAT)


def main(**kwargs):
    click.secho('>. Starting Loafer (Version={}) ...'.format(__version__),
                bold=True, fg='green')

    custom_settings = Settings(**kwargs)
    _bootstrap(custom_settings)

    click.secho('>. Hit CTRL-C to stop', bold=True, fg='yellow')

    loafer = LoaferManager(custom_settings)
    loafer.start()


#
# CLI
#

CLICK_CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


@click.group(invoke_without_command=True,
             context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('-v', default=False, is_flag=True,
              help='Verbose mode (set LOAFER_LOGLEVEL=INFO)')
@click.option('-vv', default=False, is_flag=True,
              help='Very verbose mode (set LOAFER_LOGLEVEL=DEBUG)')
@click.pass_context
def cli(context, v, vv):
    override_settings = {}
    if v:
        override_settings['LOAFER_LOGLEVEL'] = 'INFO'
    if vv:
        override_settings['LOAFER_LOGLEVEL'] = 'DEBUG'

    if context.invoked_subcommand is None:
        main(**override_settings)


@cli.command()
def version():
    """Show Loafer version"""
    click.echo('{}'.format(__version__))


@cli.command()
@click.option('--queue', default=None, help='SQS queue name ou url')
@click.option('--topic', default=None, help='SNS topic name ou arn')
@click.option('--msg', help='Message to publish (assumes json format)')
def publish(queue, topic, msg):
    """Publish messages"""
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
    click.echo('Response: {}'.format(response))
