from unittest import mock

from loafer.ext.sentry import sentry_handler


def test_sentry_handler():
    capture_exception_mocked = mock.Mock()
    handler = sentry_handler(capture_exception_mocked)
    exc = ValueError('test')
    exc_info = (type(exc), exc, None)
    delete_message = handler(exc_info, 'test')

    assert delete_message is False
    assert capture_exception_mocked.called
    capture_exception_mocked.assert_called_once_with(
        exc_info, message='test',
    )


def test_sentry_handler_delete_message():
    capture_exception_mocked = mock.Mock()
    handler = sentry_handler(capture_exception_mocked, delete_message=True)
    exc = ValueError('test')
    exc_info = (type(exc), exc, None)
    delete_message = handler(exc_info, 'test')

    assert delete_message is True
    assert capture_exception_mocked.called
    capture_exception_mocked.assert_called_once_with(
        exc_info, message='test',
    )
