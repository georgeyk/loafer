Usage
-----

Loafer provides a simple CLI interface.

Check the full list of options by running ``loafer --help``.


Examples
~~~~~~~~

* Starting loafer::

    $ loafer

* Add ``source`` and ``handler`` parameters (all parameters are optional)::

  $ loafer --source my-queue-name --handler loafer.example.jobs.async_example_job


* Publishing a message to SNS/SQS (you should see some logging messages)::

    # To SQS
    $ loafer publish_sqs --queue a-queue-name --msg 'foobar'

    # To SNS (considering, the queue we consume are subscribed to topic)
    $ loafer publish_sns --topic a-topic-name --msg 'foobar'
