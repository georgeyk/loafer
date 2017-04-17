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

Any other exception will be redirected to an ``error_handler``, see more
:doc:`error_handlers`.

The default ``error_handler`` will log the error and **not** acknowledge the message.

For some generic handlers that can give you starting point, take a look at
:doc:`generic_handlers` section.


Class-based handlers
~~~~~~~~~~~~~~~~~~~~


You can also write handlers using classes. The class should implement a
``handle`` coroutine/method::

    class MyHandler:

        async def handle(self, message, *args):
            ... code ...
            return True

         def stop(self):
            ... clean-up code ...


The method ``stop`` is optional and will be called before loafer shutdown it's
execution. Note that ``stop`` is not a coroutine.

When configuring your :doc:`routes`, you can set ``handler`` to an instance of
``MyHandler`` instead of the ``handle`` method (but both ways work)::

    Route(handler=MyHandler(), ...)
    # or
    Route(handler=MyHandler().handle)
