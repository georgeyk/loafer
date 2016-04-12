Settings
--------

All configuration is done using environment variables.

You can also create an ``.env`` or ``*.cfg`` file in your project root, they
will be loaded automatically.

Here is a sample ``.env`` file::

    LOAFER_DEFAULT_QUEUE_NAME=test-images


All the possible configuration keys and its default values are listed below
(entries without default values are marked as **required**):

.. list-table:: Settings table
    :header-rows: 1

    * - Key
      - Default value
    * - LOAFER_LOG_FORMAT
      - '%(format)s'


AWS
~~~

To configure AWS access, check `boto3 configuration`_ or export::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret> 


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration 
