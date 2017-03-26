from unittest import mock

from asynctest import CoroutineMock
import pytest

from loafer.routes import Route


def test_provider():
    provider = mock.Mock()
    route = Route(provider, handler=mock.Mock())
    assert route.provider is provider


def test_name():
    route = Route('whatever', handler=mock.Mock(), name='foo')
    assert route.name == 'foo'


def test_message_translator():
    route = Route('foo', 'invalid', message_translator=mock.Mock())
    assert isinstance(route.message_translator, mock.Mock)


def test_default_message_translator():
    route = Route('foo', mock.Mock())
    assert route.message_translator is None


def test_apply_message_translator():
    translator = mock.Mock(translate=mock.Mock(return_value={'content': 'foobar', 'metadata': {}}))
    route = Route('foo', mock.Mock(), message_translator=translator)
    translated = route.apply_message_translator('message')
    assert translated['content'] == 'foobar'
    assert translated['metadata'] == {}
    assert translator.translate.called
    translator.translate.assert_called_once_with('message')


def test_apply_message_translator_error():
    translator = mock.Mock(translate=mock.Mock(return_value={'content': '', 'metadata': {}}))
    route = Route('foo', mock.Mock(), message_translator=translator)
    with pytest.raises(ValueError):
        route.apply_message_translator('message')
        assert translator.translate.called
        translator.translate.assert_called_once_with('message')


@pytest.mark.asyncio
async def test_error_handler_unset():
    route = Route('foo', mock.Mock())
    exc = TypeError()
    result = await route.error_handler(type(exc), exc, 'whatever')
    assert result is False


@pytest.mark.asyncio
async def test_error_handler():
    attrs = {}

    def error_handler(exc_type, exc, message):
        attrs['exc_type'] = exc_type
        attrs['exc'] = exc
        attrs['message'] = message
        return True

    # we cant mock regular functions in error handlers, because it will
    # be checked with asyncio.iscoroutinefunction() and pass as coro
    route = Route('foo', mock.Mock(), error_handler=error_handler)
    exc = TypeError()
    result = await route.error_handler(type(exc), exc, 'whatever')
    assert result is True
    assert attrs['exc_type'] == type(exc)
    assert attrs['exc'] == exc
    assert attrs['message'] == 'whatever'


@pytest.mark.asyncio
async def test_error_handler_coroutine():
    error_handler = CoroutineMock(return_value=True)
    route = Route('foo', mock.Mock(), error_handler=error_handler)
    exc = TypeError()
    result = await route.error_handler(type(exc), exc, 'whatever')
    assert result is True
    assert error_handler.called
    error_handler.assert_called_once_with(type(exc), exc, 'whatever')


# FIXME: Improve all test_deliver* tests

@pytest.mark.asyncio
async def test_deliver():
    attrs = {}

    def test_handler(*args, **kwargs):
        attrs['args'] = args
        attrs['kwargs'] = kwargs
        return True

    route = Route('foo-queue', handler=test_handler)
    message = 'test'
    result = await route.deliver(message)

    assert result is True
    assert message in attrs['args']


@pytest.mark.asyncio
async def test_deliver_with_coroutine():
    mock_handler = CoroutineMock(return_value=False)
    route = Route('foo-queue', mock_handler)
    message = 'test'
    result = await route.deliver(message)
    assert result is False
    assert mock_handler.called
    assert message in mock_handler.call_args[0]


@pytest.mark.asyncio
async def test_deliver_with_message_translator():
    mock_handler = CoroutineMock(return_value=True)
    route = Route('foo-queue', mock_handler)
    route.apply_message_translator = mock.Mock(return_value={'content': 'whatever', 'metadata': {}})
    result = await route.deliver('test')
    assert result is True
    assert route.apply_message_translator.called
    assert mock_handler.called
    mock_handler.assert_called_once_with('whatever', {})
