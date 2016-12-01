import json
import logging

import click

from .conf import settings
from .manager import LoaferManager
from .ext.aws.publisher import sqs_publish, sns_publish


def _bootstrap():
    logging.basicConfig(level=settings.LOAFER_LOGLEVEL,
                        format=settings.LOAFER_LOG_FORMAT)

    click.echo('>. Routes:')
    for route in settings.LOAFER_ROUTES:
        click.echo('>.\t{}:'.format(route['name']))
        click.echo('>.\t\tSource: {}'.format(route['source']))
        click.echo('>.\t\tHandler: {}'.format(route['handler']))
        click.echo('>.\t\tMessage Translator: {}'.format(route['message_translator']))
        click.echo('>.\t\tConsumer Options: {}'.format(settings.LOAFER_DEFAULT_CONSUMER_OPTIONS))


def main(**kwargs):
    click.secho('>. Starting Loafer ...', bold=True, fg='green')

    _bootstrap()

    click.secho('>. Hit CTRL-C to stop', bold=True, fg='yellow')

    loafer = LoaferManager()
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
@click.option('--max-threads', default=None, type=int,
              help='Maximum threads, overrides LOAFER_MAX_THREAD_POOL')
@click.option('--source', default=None,
              help='The route source, updates the default route source')
@click.option('--handler', default=None,
              help='The route handler, updates the default route handler')
@click.option('--translator', default=None,
              help='The message translator class, updates the default route message translator')
@click.option('--consumer-opts', default=None,
              help='The consumer options (assumes json), overrides LOAFER_DEFAULT_CONSUMER_OPTIONS')
@click.pass_context
def cli(context, v, vv, max_threads, source, handler, translator, consumer_opts):
    if v:
        settings.LOAFER_LOGLEVEL = 'INFO'
    if vv:
        settings.LOAFER_LOGLEVEL = 'DEBUG'
    if max_threads and max_threads >= 1:
        settings.LOAFER_MAX_THREAD_POOL = max_threads
    if source:
        settings.LOAFER_ROUTES[0]['source'] = source
    if handler:
        settings.LOAFER_ROUTES[0]['handler'] = handler
    if translator:
        settings.LOAFER_ROUTES[0]['message_translator'] = translator
    if consumer_opts:
        opts = json.loads(consumer_opts)
        settings.LOAFER_DEFAULT_CONSUMER_OPTIONS = opts

    if context.invoked_subcommand is None:
        main()


@cli.command()
@click.option('--queue', default=None, help='SQS queue name ou url')
@click.option('--msg', help='Message to publish (assumes json format)')
def publish_sqs(queue, msg):
    """Publish messages to AWS SQS"""
    response = sqs_publish(queue, json.dumps(msg))
    click.echo('Response: {}'.format(response))


@cli.command()
@click.option('--topic', default=None, help='SNS topic name ou arn')
@click.option('--msg', help='Message to publish (assumes json format)')
def publish_sns(topic, msg):
    """Publish messages to AWS SNS"""
    # We need this validation because our sns_publish always use json format
    try:
        json.loads(msg)
    except json.decoder.JSONDecodeError:
        click.secho('"{}" should be a valid json'.format(msg), fg='red')
    else:
        response = sns_publish(topic, msg)
        click.echo('Response: {}'.format(response))
