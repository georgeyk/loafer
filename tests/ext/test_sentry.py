from unittest import mock

from loafer.ext.sentry import sentry_handler


def test_sentry_handler():
    mock_scope = mock.MagicMock()
    sdk_mocked = mock.Mock()
    sdk_mocked.push_scope.return_value = mock_scope

    handler = sentry_handler(sdk_mocked)
    exc = ValueError("test")
    exc_info = (type(exc), exc, None)
    delete_message = handler(exc_info, "test")

    assert delete_message is False
    assert sdk_mocked.push_scope.called
    mock_scope.__enter__.return_value.set_extra.assert_called_once_with(
        "message", "test"
    )
    sdk_mocked.capture_exception.assert_called_once_with(exc_info)


def test_sentry_handler_delete_message():
    mock_scope = mock.MagicMock()
    sdk_mocked = mock.Mock()
    sdk_mocked.push_scope.return_value = mock_scope

    handler = sentry_handler(sdk_mocked, delete_message=True)
    exc = ValueError("test")
    exc_info = (type(exc), exc, None)
    delete_message = handler(exc_info, "test")

    assert delete_message is True
    assert sdk_mocked.push_scope.called
    mock_scope.__enter__.return_value.set_extra.assert_called_once_with(
        "message", "test"
    )
    sdk_mocked.capture_exception.assert_called_once_with(exc_info)
