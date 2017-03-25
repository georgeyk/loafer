Error Handlers
--------------

Every ``Route`` implements a coroutine ``error_handler`` that can be used as an error hook.
This hook are called when unhandled exceptions happen and by default it will only log the
error and **not** acknowledge the message.

``Route`` accepts a callable parameter, ``error_handler``, so you can pass a custom function or
coroutine to replace the default error handler behavior.

The callable should be similar to::

    async def custom_error_handler(exc_type, exc, message):
        ... custom code here ...
        return True

     # Route(..., error_handler=custom_error_handler)


The return value determines if the message that originated the error will be acknowledged or not.
``True`` means acknowledge it, ``False`` will only ignore the message (default behavior).
