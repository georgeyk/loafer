# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import click

from .manager import LoaferManager
from .utils import echo


def main():
    echo('Starting loafer ...')
    echo('Hit CTRL-C to stop', bold=True)

    loafer = LoaferManager()
    loafer.start()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if context.invoked_subcommand is None:
        main()
