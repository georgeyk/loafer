Installation
============

Requirements
------------

Python 3.5+

Note::

    Some packages also needs python3.5-dev package (ubuntu) or similar


To install via pip::

    $ pip install loafer


Basic configuration
-------------------


To configure AWS access, check `boto3 configuration`_ or export (see `boto3 envvars`_)::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>
    $ export AWS_DEFAULT_REGION=sa-east-1  # for example


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
.. _boto3 envvars: http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variable-configuration


There are more two environment variables you'll need to set::

    $ export LOAFER_DEFAULT_ROUTE_SOURCE=my-queue
    $ export LOAFER_DEFAULT_ROUTE_HANDLER=loafer.example.jobs.async_example_job

The ``LOAFER_DEFAULT_ROUTE_SOURCE`` is the name of SQS queue you'll consume messages from.

The ``LOAFER_DEFAULT_ROUTE_HANDLER`` is a full path of the callable that will receive the message.

The value set by default in handler configuration is ``loafer.example.jobs.async_example_job``
and it will only log the received message with ``warning`` level.
