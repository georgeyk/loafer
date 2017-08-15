FAQ
---


**1. How do I run I/O blocking code that's not a coroutine ?**

   Any code that is blocking and not a coroutine could run in a separate thread.

   It's not recommended, but it looks like this::

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, your_callable, your_callable_args)
    # Important: do not close/stop the loop


**2. How to integrate with newrelic ?**

    The `newrelic`_ should be the primary source of information.
    One alternative is to use environment variables ``NEW_RELIC_LICENSE_KEY`` and
    ``NEW_RELIC_APP_NAME`` and for every handler::

        import newrelic.agent

        @newrelic.agent.background_task()
        def some_code(...):
            ...


**3. Using different regions/credentials with SQSRoute/SNSRoute ?**

    ``SQSRoute``/``SNSRoute`` instantiates ``loafer.ext.aws.providers.SQSProvider``,
    therefore you can dinamically set these options to any of :doc:`providers` available.

    An example with explicity AWS credentials and provider options would look like::

        from loafer.ext.aws.routes import SQSRoute

        route = SQSRoute(
            'test-queue-name', name='my-route', handler=some_handler,
            provider_options={
                'aws_access_key_id': my_aws_access_key,
                'aws_secret_access_key': my_secret_key,
                'region_name': 'sa-east-1',
                'options': {'WaitTimeSeconds': 3},
            },
        )

..  _newrelic: https://docs.newrelic.com/docs/agents/python-agent/getting-started/introduction-new-relic-python
