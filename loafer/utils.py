# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import importlib

import click


def echo(message, **kwargs):
    msg = '>. {}'.format(message)
    if kwargs:
        msg = click.style(msg, **kwargs)
    click.echo(msg)


def import_callable(full_name):
    package, *name = full_name.rsplit('.', 1)
    try:
        module = importlib.import_module(package)
    except ValueError as exc:
        raise ImportError('Error trying to import {!r}'.format(full_name)) from exc

    if name:
        handler = getattr(module, name[0])
    else:
        handler = module

    if not callable(handler):
        raise ImportError('{!r} should be callable'.format(full_name))

    return handler
