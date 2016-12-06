Exceptions and error handling
-----------------------------

All exceptions are defined at ``loafer.exceptions`` module.

A description of all the exceptions:


* ``ConsumerError``: a fatal error from a consumer instance.
  Loafer will stop all operations and shutdown.

* ``ConfigurationError``: a configuration error. Loafer will
  stop all operations and shutdown.

* ``IgnoreMessage``: if the handler raises this exception, the message will
  be ignored and not acknowledged.

* ``RejectMessage``: if the handler raises this exception, the message will
  be rejected and acknowledged (e.g., the message will be deleted).

* ``DeleteMessage``: alias to ``RejectMessage``.

* ``LoaferException``: the base exception for ``IgnoreMessage``, ``RejectMessage`` and
  ``DeleteMessage``.


At the message translation phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the message translator returns an invalid message content or an unhandled
exception:

1. The message will not be delivered to ``handler``
2. The message will be ignored (e.g., will not be deleted)


At the handler processing phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``handler`` can use ``IgnoreMessage`` or ``RejectMessage``/``DeleteMessage`` to explicity
determine how the message will be handled.

Any unhandled exceptions will have the same effect of ``IgnoreMessage``, but
is advised to ``handler`` treat its own errors in case of change of behavior
in the future.


Error handler hook
~~~~~~~~~~~~~~~~~~

Every ``Route`` implements a coroutine ``error_handler`` that can be used as an error hook.
This hook are called when unhandled exceptions happen and by default it will only log the
error and ignore the message.

``Route`` accepts a callable parameter, ``error_handler``, so you can pass a custom function or
coroutine to replace the default error handler behavior.

The callable should be similar to::

    async def custom_error_handler(exc_type, exc, message):
        ... custom code here ...
        return True

     # Route(..., error_handler=custom_error_handler)


The return value determines if the message that originated the error will be acknowledged or not.
``True`` means acknowledge it, ``False`` will only ignore the message (default behavior).


Message deletion
~~~~~~~~~~~~~~~~

The message will be deleted (acknowledged):

1. When the ``handler`` raises ``RejectMessage``/``DeleteMessage``
2. Succesfull executions of ``handler``
