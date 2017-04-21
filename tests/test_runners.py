from unittest import mock

from concurrent.futures import CancelledError

from loafer.runners import LoaferRunner


def test_runner_start():
    runner = LoaferRunner(loop=mock.Mock())
    runner.start()
    assert runner.loop.run_forever.called


def test_runner_start_run_until_complete():
    runner = LoaferRunner(loop=mock.Mock())
    runner.stop = mock.Mock()
    runner.start(run_forever=False)
    assert runner.loop.run_until_complete.called
    assert runner.stop.called


def test_runner_stop():
    runner = LoaferRunner(loop=mock.Mock())
    runner.stop()
    assert runner.loop.stop.called


def test_runner_stop_with_callback():
    callback = mock.Mock()
    runner = LoaferRunner(loop=mock.Mock(), on_stop_callback=callback)
    runner.stop()
    assert runner.loop.stop.called
    assert callback.called


def test_runner_with_cancelled_error():
    runner = LoaferRunner(loop=mock.Mock())
    runner.loop.run_forever.side_effect = CancelledError
    runner.start()
    assert runner.loop.run_forever.called
    assert runner.loop.close.called
