# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import pytest

from loafer.example.consumer import RandomIntConsumer


@pytest.fixture
def consumer():
    return RandomIntConsumer()


@pytest.mark.asyncio
async def test_consume(consumer):
    messages = await consumer.consume()
    assert len(messages) == 1
    assert messages[0] > 0


@pytest.mark.asyncio
async def test_confirm_message(consumer):
    confirmation = await consumer.confirm_message(1)
    assert confirmation is True
