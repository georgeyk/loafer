# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import json
from unittest import mock

from click.testing import CliRunner

import pytest

from loafer import conf
from loafer.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def local_settings():
    return conf.Settings()


def test_verbose(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['-v'])
        assert settings.LOAFER_LOGLEVEL == 'INFO'


def test_very_verbose(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['-vv'])
        assert settings.LOAFER_LOGLEVEL == 'DEBUG'


def test_max_jobs(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--max-jobs', '20'])
        assert settings.LOAFER_MAX_JOBS == 20


def test_max_jobs_error(runner, local_settings):
    result = runner.invoke(cli, ['--max-jobs', 'a'])
    assert isinstance(result.exception, SystemExit)

    with mock.patch('loafer.cli.settings', local_settings) as settings:
        result = runner.invoke(cli, ['--max-jobs', '0'])
        # preserves default value
        assert settings.LOAFER_MAX_JOBS == 10


def test_max_threads(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--max-threads', '20'])
        assert settings.LOAFER_MAX_THREAD_POOL == 20


def test_max_threads_error(runner, local_settings):
    result = runner.invoke(cli, ['--max-threads', 'a'])
    assert isinstance(result.exception, SystemExit)

    with mock.patch('loafer.cli.settings', local_settings) as settings:
        result = runner.invoke(cli, ['--max-threads', '0'])
        # preserves default value
        assert settings.LOAFER_MAX_THREAD_POOL is None


def test_source(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--source', 'foobar'])
        routes = settings.LOAFER_ROUTES
        assert routes[0]['source'] == 'foobar'


def test_handler(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--handler', 'foobar'])
        routes = settings.LOAFER_ROUTES
        assert routes[0]['handler'] == 'foobar'


def test_translator(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--translator', 'foobar'])
        routes = settings.LOAFER_ROUTES
        assert routes[0]['message_translator'] == 'foobar'


def test_consumer(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        runner.invoke(cli, ['--consumer', 'foobar'])
        assert settings.LOAFER_DEFAULT_CONSUMER_CLASS == 'foobar'


def test_consumer_opts(runner, local_settings):
    with mock.patch('loafer.cli.settings', local_settings) as settings:
        for opt in [{}, '1', [], '{"key": "value"}', '""']:
            runner.invoke(cli, ['--consumer-opts', str(opt)])
            assert settings.LOAFER_DEFAULT_CONSUMER_OPTIONS == json.loads(str(opt))


def test_consumer_opts_error(runner):
    for opt in ['test', '123:123']:
        result = runner.invoke(cli, ['--consumer-opts', opt])
        assert isinstance(result.exception, json.decoder.JSONDecodeError)
