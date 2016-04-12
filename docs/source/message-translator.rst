Message Translator
------------------

The message translator is the contract between the consumer and the handler.

In the future it will also help the dispatcher choose the message destination handler.

At the moment, the message translator is responsible for:

* Receive the raw message from consumer
* Translate the message in a appropriate format to message handler
