Message Translators
-------------------

The message translator receives a "raw message" and process it to a suitable
format expected by the ``handler``.

The "raw message" is the message received by the ``provider`` "as-is" and
it might be delivered without any processing if the message translator was
not set.

In some cases, you should explicitly set ``message_translator=None`` to disable
any configured translators.


Implementation
~~~~~~~~~~~~~~

The message translator class should subclass ``AbstractMessageTranslator`` and
implement the method ``translate`` like::


    from loafer.message_translators import AbstractMessageTranslator


    class MyMessageTranslator(AbstractMessageTranslator):

        def translate(self, message):
            return {'content': int(message), 'metadata': {}}


And it should return a dictionary in the format::

    return {'content': processed_message, 'metadata': {}}

The ``processed_message`` and ``metadata`` (optional) will be delivered to
``handler``.

If ``processed_message`` is ``None`` (or empty) the message will cause
``ValueError`` exception.

All the exceptions in message translation will be caught by the configured
:doc:`error_handlers`.

The existing message translators will be described below.


loafer.message_translators.StringMessageTranslator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A message translator that translates the given message to a string (python `str`).


loafer.ext.aws.message_translators.SQSMessageTranslator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A message translator that translates SQS messages. The expected message body
is a **json** payload that will be decoded with ``json.loads``.

All the keys will be kept in ``metadata`` key ``dict`` (except ``Body``
that was previously translated).


loafer.ext.aws.message_translators.SNSMessageTranslator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A message translator that translates SQS messages that came from SNS topic.
The expected notification message is a **json** payload that will be decoded
with ``json.loads``.

SNS notifications wraps (and encodes) the message inside the body of a SQS
message, so the ``SQSMessageTranslator`` will fail to properly
translate those messages (or at least, fail to translate to the expected format).


All the keys will be kept in ``metadata`` key ``dict`` (except ``Body``).


For more details about message translators usage, check the :doc:`routes` examples.
