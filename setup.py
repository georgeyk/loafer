# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from setuptools import setup

setup(
    name='loafer',
    version='0.0.1',
    entry_points='''
    [console_scripts]
    loafer=loafer.cli:cli
    ''',
)
