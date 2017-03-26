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

..  _newrelic: https://docs.newrelic.com/docs/agents/python-agent/getting-started/introduction-new-relic-python
