Tutorial
--------

For this tutorial we assume you already have ``loafer`` installed and your
aws credentials configured.

Let's create a repository named ``foobar`` with the following structure::

    foobar/
        handlers.py
        routes.py
        __main__.py
        __init__.py  # empty file


The ``handlers.py``::

    import asyncio

    async def print_handler(message, *args):
        print('message is {}'.format(message))
        print('args is {}'.format(args))

        # mimic IO processing
        await asyncio.sleep(0.1)
        return True


    async def error_handler(exc_info, message):
        print('exception {} received'.format(exc_info))
        # do not delete the message that originated the error
        return  False


The ``routes.py``::

    from loafer.ext.aws.routes import SQSRoute
    from .handlers import print_handler, error_handler

    # assuming a queue named "loafer-test"
    routes = (
        SQSRoute('loafer-test', {'options': {'WaitTimeSeconds': 3}},
                 handler=print_handler,
                 error_handler=error_handler),
    )


The ``__main__.py``::

    from loafer.managers import LoaferManager
    from .routes import routes

    manager = LoaferManager(routes=routes)
    manager.run()


To execute::

    $ python -m foobar


To see any output, publish some messages using AWS dashboard or utilities like `awscli`_.

For example::

    $ aws sqs send-message --queue-url http://<url-part>/loafer-test --message-body '{"key": true}'

.. _awscli: https://github.com/aws/aws-cli
