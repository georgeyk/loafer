# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

import click
from prettyconf import config

from .manager import LoaferManager
from .utils import echo


logger = logging.getLogger(__name__)


def _setup_logging():
        default_log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=config('LOGLEVEL', default='INFO'),
                            format=config('LOG_FORMAT', default=default_log_format))


def main():
    _setup_logging()
    echo('Starting loafer ...')
    echo('Hit CTRL-C to stop', bold=True)

    loafer = LoaferManager()
    loafer.start()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if context.invoked_subcommand is None:
        main()
