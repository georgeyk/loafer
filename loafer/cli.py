# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

import click

from .conf import settings
from .manager import LoaferManager
from .utils import echo


logger = logging.getLogger(__name__)


def _bootstrap():
    logging.basicConfig(level=settings.LOGLEVEL, format=settings.LOG_FORMAT)


def main():
    _bootstrap()

    echo('Starting loafer ...')
    echo('Hit CTRL-C to stop', bold=True)

    loafer = LoaferManager()
    loafer.start()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if context.invoked_subcommand is None:
        main()
