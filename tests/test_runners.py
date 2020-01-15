import asyncio
from unittest import mock

import pytest

from loafer.runners import LoaferRunner


@mock.patch('loafer.runners.LoaferRunner.loop', new_callable=mock.PropertyMock)
def test_runner_start(loop_mock):
    runner = LoaferRunner()

    runner.start()

    assert loop_mock.return_value.run_forever.called


@mock.patch('loafer.runners.LoaferRunner.loop', new_callable=mock.PropertyMock)
def test_runner_start_with_debug(loop_mock):
    runner = LoaferRunner()

    runner.start(debug=True)

    loop_mock.return_value.set_debug.assert_called_once_with(enabled=True)


@mock.patch('loafer.runners.LoaferRunner.loop', new_callable=mock.PropertyMock)
def test_runner_start_and_stop(loop_mock):
    runner = LoaferRunner()
    runner.stop = mock.Mock()

    runner.start()

    assert runner.stop.called
    assert loop_mock.return_value.run_forever.called
    assert loop_mock.return_value.close.called


@mock.patch('loafer.runners.LoaferRunner.loop', new_callable=mock.PropertyMock)
def test_runner_prepare_stop(loop_mock):
    loop_mock.return_value.is_running.return_value = True
    runner = LoaferRunner()

    runner.prepare_stop()

    loop_mock.return_value.stop.assert_called_once_with()


@mock.patch('loafer.runners.asyncio.get_event_loop')
def test_runner_prepare_stop_already_stopped(get_loop_mock):
    loop = mock.Mock(is_running=mock.Mock(return_value=False))
    get_loop_mock.return_value = loop
    runner = LoaferRunner()

    runner.prepare_stop()

    loop.is_running.assert_called_once_with()
    assert loop.stop.called is False


@mock.patch('loafer.runners.asyncio.get_event_loop')
def test_runner_stop_with_callback(loop_mock):
    callback = mock.Mock()
    runner = LoaferRunner(on_stop_callback=callback)

    runner.stop()

    assert callback.called


def test_runner_stop_dont_raise_cancelled_error():
    async def some_coro():
        await asyncio.sleep(1)
        raise asyncio.CancelledError()

    runner = LoaferRunner()
    loop = runner.loop
    task = loop.create_task(some_coro())
    runner.stop()
    assert task.cancelled() is True
    with pytest.raises(asyncio.CancelledError):
        task.exception()
