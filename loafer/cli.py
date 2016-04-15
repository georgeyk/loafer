# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import json
import logging

import click

from . import __version__
from .conf import settings
from .manager import LoaferManager
from .aws.publisher import Publisher


logger = logging.getLogger(__name__)


def _bootstrap():
    logging.basicConfig(level=settings.LOAFER_LOGLEVEL,
                        format=settings.LOAFER_LOG_FORMAT)


def main(**kwargs):
    click.secho('>. Starting Loafer (Version={}) ...'.format(__version__),
                bold=True, fg='green')

    _bootstrap()

    click.secho('>. Hit CTRL-C to stop', bold=True, fg='yellow')

    loafer = LoaferManager()
    loafer.start()


#
# CLI
#

CLICK_CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


def show_version(ctx, param, value):
    """Show Loafer version"""
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group(invoke_without_command=True,
             context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('-v', default=False, is_flag=True,
              help='Verbose mode (set LOAFER_LOGLEVEL=INFO)')
@click.option('-vv', default=False, is_flag=True,
              help='Very verbose mode (set LOAFER_LOGLEVEL=DEBUG)')
@click.option('--version', is_flag=True, is_eager=True, expose_value=False,
              callback=show_version, help="Show Loafer's version and exit")
@click.option('--source', default=None,
              help='The route source, updates the default route source')
@click.option('--handler', default=None,
              help='The route handler, updates the default route handler')
@click.option('--translator', default=None,
              help='The message translator class, updates the default route message translator')
@click.option('--consumer', default=None,
              help='The consumer class, overrides LOAFER_DEFAULT_CONSUMER_CLASS')
@click.option('--consumer-opts', default=None,
              help='The consumer options (assumes json), overrides LOAFER_DEFAULT_CONSUMER_OPTIONS')
@click.pass_context
def cli(context, v, vv, source, handler, translator, consumer, consumer_opts):
    if v:
        settings.LOAFER_LOGLEVEL = 'INFO'
    if vv:
        settings.LOAFER_LOGLEVEL = 'DEBUG'
    if source:
        settings.LOAFER_ROUTES[0]['source'] = source
    if handler:
        settings.LOAFER_ROUTES[0]['handler'] = handler
    if translator:
        settings.LOAFER_ROUTES[0]['message_translator'] = translator
    if consumer:
        settings.LOAFER_DEFAULT_CONSUMER_CLASS = consumer
    if consumer_opts:
        opts = json.loads(consumer_opts)
        settings.LOAFER_DEFAULT_CONSUMER_OPTIONS = opts

    if context.invoked_subcommand is None:
        main()


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
