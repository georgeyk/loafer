Handlers
--------

Handlers are callables that receives the message.

The ``handler`` signature should be similar to::

    async def my_handler(message, metadata):
        ... code ...
        return True # or False

Where ``message`` is the message to be processed and ``metadata`` is a ``dict``
with metadata information.

The ``async def`` is the python coroutine syntax, but regular functions
can also be used, but will run in a thread, outside the event loop.

The return value indicates if the ``handler`` successfully processed the
message or not.
By returning ``True`` the message will be acknowledged (deleted).

Another way to acknowledge messages inside a handler is to raise
``DeleteMessage`` exception.

Any other exception will be redirected to an ``error_handler``, see :doc:`error_handlers`.

The default ``error_handler`` will log the error and **not** acknowledge the message.
