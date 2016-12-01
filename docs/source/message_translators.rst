Message Translators
-------------------

The message translator receives a "raw message" and process it to a suitable
format expected by the ``handler``.

The "raw message" is the message received by the ``consumer`` "as-is" and
it might be delivered without any processing if the message translator was
not set.


Implementation
~~~~~~~~~~~~~~

The message translator class should implement the method ``translate`` like::

    class MyMessageTranslator(object):

        def translate(self, message):
            return {'content': int(message)}

And it should return a dictionary in the format::

    return {'content': processed_message}

The ``processed_message`` is the message delivered to ``handler``.

In the example above, message is supposed to be an integer and will be
delivered as integer too.

The ``message`` parameter in ``def translate`` is always a string object.

If ``processed_message`` is ``None`` the message will be ignored and not
acknowledged.

Unhandled errors also makes the message to be ignored, but it's a good practice
to handle those errors.
