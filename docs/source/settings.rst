Settings
--------

All configuration is done using environment variables.

You can also create an ``.env`` or ``*.cfg`` file in your project root, they
will be loaded automatically.

Here is a sample ``.env`` file::

    LOAFER_DEFAULT_ROUTE_SOURCE=my-queue-name
    LOAFER_DEFAULT_ROUTE_HANDLER=loafer.example.jobs.async_example_job


All the possible configuration keys and its default values are listed below
(entries without default values are marked as **required**):

.. list-table:: Settings table
    :header-rows: 1

    * - Key
      - Default value
    * - LOAFER_LOG_FORMAT
      - '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    * - LOAFER_MAX_JOBS
      - 10
    * - LOAFER_MAX_THREAD_POOL
      - None
    * - LOAFER_DEFAULT_ROUTE_NAME
      - 'default'
    * - LOAFER_DEFAULT_ROUTE_SOURCE
      - **required**
    * - LOAFER_DEFAULT_ROUTE_HANDLER
      - 'loafer.example.jobs.async_example_job'
    * - LOAFER_DEFAULT_CONSUMER_CLASS
      - 'loafer.ext.aws.consumer.Consumer'
    * - LOAFER_DEFAULT_CONSUMER_OPTIONS
      - {'WaitTimeSeconds: 5, 'MaxNumberOfMessages': 5}


The ``LOAFER_MAX_JOBS`` is the number of concurrent ``handler`` executions.

The ``LOAFER_MAX_THREAD_POOL`` if not set, are determined automatically by
the number of cores in the machine. Threads are used to execute ``non-asyncio``
code.

All variables that requires a ``class`` or ``callable`` must be a full name, e.g.,
we must be able to import it.


AWS
~~~

To configure AWS access, check `boto3 configuration`_ or export (see `boto3 envvars`_)::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>
    $ export AWS_DEFAULT_REGION=sa-east-1  # for example


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
.. _boto3 envvars: http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variable-configuration
