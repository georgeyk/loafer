# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import click


def echo(message, **kwargs):
    msg = '>. {}'.format(message)
    if kwargs:
        msg = click.style(msg, **kwargs)
    click.echo(msg)
