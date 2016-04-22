FAQ
---


**1. How do I run I/O blocking code that's not a coroutine ?**

   Any code that is blocking and not a coroutine could run in a separate thread.

   It's not recommended, but it looks like this::

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, your_callable, your_callable_args)
    # Important: do not close/stop the loop
