import pytest
from unittest.mock import Mock

from asynctest import Mock as AsyncMock  # flake8: NOQA
from asynctest import CoroutineMock

from loafer.route import Route


@pytest.fixture
def route():
    message_translator = Mock(translate=Mock(return_value={'content': 'message'}))
    route = AsyncMock(source='queue', message_handler='handler',
                      message_translator=message_translator, spec=Route)
    return route


@pytest.fixture
def consumer():
    return CoroutineMock(consume=CoroutineMock(return_value=['message']),
                         confirm_message=CoroutineMock())
