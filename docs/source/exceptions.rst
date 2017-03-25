Exceptions
----------

All exceptions are defined at ``loafer.exceptions`` module.

A description of all the exceptions:


* ``ProviderError``: a fatal error from a provider instance.
  Loafer will stop all operations and shutdown.

* ``ConfigurationError``: a configuration error. Loafer will
  stop all operations and shutdown.

* ``DeleteMessage``: if any :doc:`handlers` raises this exception, the message will
  be rejected and acknowledged (the message will be deleted).

* ``LoaferException``: the base exception for ``DeleteMessage``.
