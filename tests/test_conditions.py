from unittest import mock

import asynctest
import pytest

from loafer.conditions import Retry


def test_retry():
    retry = Retry()

    assert retry.exceptions
    assert retry._tries == retry.max_tries
    assert retry.delay == 0


def test_retry_invalid_tries():
    with pytest.raises(AssertionError):
        Retry(tries=0)


@pytest.mark.asyncio
async def test_deliver_two_tries():
    retry = Retry(tries=2)
    route_mock = mock.Mock(_deliver=asynctest.CoroutineMock(side_effect=NotImplementedError))

    with pytest.raises(NotImplementedError):
        await retry.deliver(route_mock, {})

    assert route_mock._deliver.await_count == 2


@pytest.mark.asyncio
@asynctest.patch('loafer.conditions.asyncio.sleep')
async def test_deliver_two_tries_with_delay(sleep_mock):
    retry = Retry(tries=3, delay=1)
    route_mock = mock.Mock(_deliver=asynctest.CoroutineMock(side_effect=NotImplementedError))

    with pytest.raises(NotImplementedError):
        await retry.deliver(route_mock, {})

    assert route_mock._deliver.await_count == 3
    assert sleep_mock.await_count == 2
    sleep_mock.assert_any_call(1)
