from unittest import mock

import pytest

from loafer.exceptions import RejectMessage, IgnoreMessage
from examples.jobs import (example_job, async_example_job,
                           reject_message_job, ignore_message_job,
                           random_int_job)


def test_example_job():
    with mock.patch('examples.jobs.logger') as mock_logger:
        example_job()
        assert mock_logger.warning.called


@pytest.mark.asyncio
async def test_async_example_job():
    with mock.patch('examples.jobs.logger') as mock_logger:
        await async_example_job()
        assert mock_logger.warning.called


@pytest.mark.asyncio
async def test_reject_message_job():
    with pytest.raises(RejectMessage):
        await reject_message_job()


@pytest.mark.asyncio
async def test_ignore_message_job():
    with pytest.raises(IgnoreMessage):
        await ignore_message_job()


@pytest.mark.asyncio
async def test_random_int_job():
    with mock.patch('examples.jobs.logger') as mock_logger:
        await random_int_job(10)
        assert mock_logger.info.called
