Usage
-----

Loafer provides a simple CLI interface.


Examples
~~~~~~~~

* Starting loafer::

    $ loafer

* Publishing a message to SNS/SQS (you should see some logging messages)::

    # To SQS
    $ loafer publish --queue a-queue-name --msg 'foobar'

    # To SNS (considering, the queue we consume are subscribed to topic)
    $ loafer publish --topic a-topic-name --msg 'foobar'
