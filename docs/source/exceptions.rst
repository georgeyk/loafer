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


At the message translation phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the message translator returns an invalid message content or an unhandled
exception:

1. The message will not be delivered to ``handler``
2. The message will be ignored (e.g., will not be deleted)


At the handler processing phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``handler`` can use ``IgnoreMessage`` or ``RejectMessage`` to explicity
determine how the message will be handled.

Any unhandled exceptions will have the same effect of ``IgnoreMessage``, but
is advised to ``handler`` treat its own errors in case of change of behavior
in the future.


Message deletion
~~~~~~~~~~~~~~~~

The message will be deleted (acknowledged):

1. When the ``handler`` raises ``RejectMessage``
2. Succesfull executions of ``handler``
