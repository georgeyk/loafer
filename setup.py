# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from setuptools import setup

import loafer

setup(
    name='loafer',
    version=loafer.__version__,
    entry_points='''
    [console_scripts]
    loafer=loafer.cli:cli
    ''',
)
