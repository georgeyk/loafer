import pytest

from loafer.providers import AbstractProvider


@pytest.fixture
def dummy_handler():
    def handler(message, *args):
        raise AssertionError('I should not be called')

    return handler


@pytest.fixture
def dummy_provider():

    class Dummy(AbstractProvider):
        async def fetch_messages(self):
            raise AssertionError('I should not be called')

        async def confirm_message(self):
            raise AssertionError('I should not be called')

        def stop(self):
            raise AssertionError('I should not be called')

    return Dummy()
