# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from unittest import mock

import pytest

from loafer.jobs import example_job, async_example_job


def test_example_job():
    with mock.patch('loafer.jobs.logger') as mock_logger:
        example_job()
        assert mock_logger.info.called


@pytest.mark.asyncio
async def test_async_example_job():
    with mock.patch('loafer.jobs.logger') as mock_logger:
        await async_example_job()
        assert mock_logger.info.called
