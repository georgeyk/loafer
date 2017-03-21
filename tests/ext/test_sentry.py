from unittest import mock

from loafer.ext.sentry import sentry_handler


def test_sentry_handler():
    mocked_client = mock.Mock()
    handler = sentry_handler(mocked_client)
    exc = ValueError('test')
    delete_message = handler(type(exc), exc, 'test')

    assert delete_message is False
    assert mocked_client.captureException.called
    assert mocked_client.captureException.called_once_with(extra={'message': 'test'})


def test_sentry_handler_delete_message():
    mocked_client = mock.Mock()
    handler = sentry_handler(mocked_client, delete_message=True)
    exc = ValueError('test')
    delete_message = handler(type(exc), exc, 'test')

    assert delete_message is True
    assert mocked_client.captureException.called
    assert mocked_client.captureException.called_once_with(extra={'message': 'test'})
