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

You might find some configuration tips in our :doc:`../faq` as well.


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
.. _boto3 envvars: http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variable-configuration
