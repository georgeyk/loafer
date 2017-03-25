Message Translators
-------------------

The message translator receives a "raw message" and process it to a suitable
format expected by the ``handler``.

The "raw message" is the message received by the ``provider`` "as-is" and
it might be delivered without any processing if the message translator was
not set.


Implementation
~~~~~~~~~~~~~~

The message translator class should implement the method ``translate`` like::

    class MyMessageTranslator:

        def translate(self, message):
            return {'content': int(message), 'metadata': {}}

And it should return a dictionary in the format::

    return {'content': processed_message, 'metadata': {}}

The ``processed_message`` and ``metadata`` (optional) will be delivered to
``handler``.

In the example above, message is supposed to be an integer and will be
delivered as integer too.


If ``processed_message`` is ``None`` (or empty) the message will cause
``ValueError`` exception.

All the exceptions in message translation will be handled over to :doc:`error_handlers`.
