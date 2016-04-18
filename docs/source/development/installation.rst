Installation
============

Requirements
------------

Python 3.5+

Note::

    Some packages also needs python3.5-dev package (ubuntu) or similar


Development install
-------------------

After forking or checking out::

    $ cd loafer/
    $ pip install -r requirements.txt
    $ pip install -r requirements/local.txt
    $ pip install -r requirements/test.txt


To configure AWS access, check `boto3 configuration`_ or export::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration

Check the :doc:`../settings` section to see specific configurations.
