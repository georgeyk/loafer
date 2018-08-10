from unittest import mock

from loafer.runners import LoaferRunner


def test_runner_start():
    runner = LoaferRunner(loop=mock.Mock())
    runner.start()
    assert runner.loop.run_forever.called


def test_runner_start_with_debug():
    loop = mock.Mock()
    runner = LoaferRunner(loop=loop)
    runner.start(debug=True)
    assert loop.set_debug.called_once_with(enabled=True)


def test_runner_start_and_stop():
    runner = LoaferRunner(loop=mock.Mock())
    runner.stop = mock.Mock()
    runner.start(run_forever=False)
    assert runner.loop.run_forever.called
    assert runner.stop.called
    assert runner.loop.close.called


def test_runner_prepare_stop():
    runner = LoaferRunner(loop=mock.Mock())
    runner.prepare_stop()
    runner.loop.stop.assert_called_once_with()


def test_runner_prepare_stop_already_stopped():
    loop = mock.Mock(is_running=mock.Mock(return_value=False))
    runner = LoaferRunner(loop=loop)
    runner.prepare_stop()
    loop.is_running.assert_called_once_with()
    assert loop.stop.called is False


def test_runner_stop_with_callback():
    callback = mock.Mock()
    runner = LoaferRunner(loop=mock.Mock(), on_stop_callback=callback)
    runner.stop()
    assert callback.called
