Handlers
--------

Handlers are callables that receives the message.

It could be defined via ``LOAFER_DEFAULT_ROUTE_HANDLER`` setting.

The ``handler`` signature depends on the :doc:`message_translators` implementation.

Usually, it will be similar to this::

    async def my_handler(message):
        ... code ...

Where ``message`` will contain some expected message format.

The ``async def`` is the python coroutine syntax, but regular functions
can also be used, but will run in a thread, outside the event loop.

The ``handler`` does not need to return anything, but any unhandled error
will cause the message to be ignored.

Note that, if the ``handler`` silently failed, for example, if you do::

    async def my_handler(message):
        try:
            ... some code ...
        except Exception:
            pass

This will cause the message to be always acknowledged.

You can specify the message to be ignored by explicity raising ``IgnoreMessage``,
then the message will not be deleted, see :doc:`exceptions` for details.


Successfull executions of ``handler`` will acknowledge (delete) the message.
