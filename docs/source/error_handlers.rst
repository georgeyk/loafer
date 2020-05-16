Error Handlers
--------------

Every ``Route`` implements a coroutine ``error_handler`` that can be used as an error hook.
This hook are called when unhandled exceptions happen and by default it will only log the
error and **not** acknowledge the message.

``Route`` accepts a callable parameter, ``error_handler``, so you can pass a custom function or
coroutine to replace the default error handler behavior.

The callable should be similar to::

    async def custom_error_handler(exc_info, message):
        ... custom code here ...
        return True

     # Route(..., error_handler=custom_error_handler)


The return value determines if the message that originated the error will be acknowledged or not.
``True`` means acknowledge it, ``False`` will only ignore the message (default behavior).


Sentry
~~~~~~


To integrate with `sentry`_ you will need the `sdk`_ client and your account DSN.

Then you can automatically create an ``error_handler`` with the following code::

    from loafer.ext.sentry import sentry_handler
    from sentry_sdk import init, capture_message

    init(...)
    error_handler = sentry_handler(capture_message, delete_message=True)


The optional ``delete_message`` parameter controls the message acknowledgement
after the error report. By default, ``delete_message`` is ``False``.

The ``error_handler`` defined can be set on any ``Route`` instance.

.. _sentry: https://sentry.io/
.. _sdk: https://github.com/getsentry/sentry-python
