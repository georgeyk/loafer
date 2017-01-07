from unittest import mock

from loafer.runners import LoaferRunner


def test_runner_start():
    runner = LoaferRunner(loop=mock.Mock())
    runner.start()
    assert runner._loop.run_forever.called
    assert runner._loop.close.called


def test_runner_start_run_until_complete():
    runner = LoaferRunner(loop=mock.Mock())
    runner.start(run_forever=False)
    assert runner._loop.run_until_complete.called
    assert runner._loop.close.called


def test_runner_stop():
    runner = LoaferRunner(loop=mock.Mock())
    runner.stop()
    assert runner._loop.stop.called


def test_runner_stop_with_callback():
    callback = mock.Mock()
    runner = LoaferRunner(loop=mock.Mock(), on_stop_callback=callback)
    runner.stop()
    assert runner._loop.stop.called
    assert callback.called
