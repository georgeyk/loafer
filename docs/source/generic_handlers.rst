Generic Handlers
-----------------

Here are some handlers that are easy to extend or use directly.


loafer.ext.aws.handlers.SQSHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A handler that publishes messages to a SQS queue.

For instance, if we just want just redirect a message to a queue named `my-queue`::

    # in your route definition
    from loafer.ext.aws.handlers import SQSHandler

    Route(handler=SQSHandler('my-queue'), ...)

The handler assumes a message that could be json encoded (usually a `dict` instance).

You can customize this handler by subclassing it::

    class MyHandler(SQSHandler):
        queue_name = 'my-queue'

        async def handle(self, message, *args):
            text = message['text']
            return await self.publish(text, encoder=None)

In the example above, we are disabling the message encoding by passing `None`
to the `publish` coroutine.

The `encoder` parameter should be a callable that receives the message to be encoded.
By default, it assumes `json.dumps`.

Take a note how **queue_name** was set. You can configure it when instantiate
the handler or set the class attribute **queue_name**, both are valid and the
attribute is mandatory.


loafer.ext.aws.handlers.SNSHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A handler that publishes messages to a SNS topic.

This handler is very similar to `SQSHandler`, so going to a similar example::

    from loafer.ext.aws.handlers import SNSHandler

    class MyHandler(SNSHandler):
        topic_name = 'my-topic'

        async def handle(self, message, *args):
            text = message['text']
            return await self.publish(text, encoder=None)

The handler also provides a `publish` coroutine with an `encoder` parameter
that works in the same way, except it will publish in a SNS topic instead a queue.

The `SNSHandler` also assumes a message that could be json encoded and the encoder default to `json.dumps`.

The **topic_name** is also mandatory and should be configured in the class
definition or when creating the handler instance.
