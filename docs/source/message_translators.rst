Message Translators
-------------------

The message translator receives a "raw message" and process it to a suitable
format expected by the ``handler``.

The "raw message" is the message received by the ``consumer`` "as-is".

It could be defined via ``LOAFER_DEFAULT_MESSAGE_TRANSLATOR_CLASS`` setting.


Implementation
~~~~~~~~~~~~~~

The message translator class should implement the method ``translate`` like::

    def translate(self, message):

And it should return a dictionary in the format::

    return {'content': processed_message}

The ``processed_message`` is the message delivered to ``handler``.

If ``processed_message`` is ``None`` the message will be ignored and not
acknowledged.

Unhandled errors also makes the message to be ignored.
