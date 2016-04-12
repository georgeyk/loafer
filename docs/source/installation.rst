Installation
============

Requirements
------------

Python 3.5+

Note::

    Some packages also needs python3.5-dev package (ubuntu) or similar


Other requirements could be found at requirements folder in the project tree. 


Development install
--------------------

After forking or checking out::

    $ cd loafer/
    $ pip install -r requirements.txt
    $ pip install -r requirements/local.txt


To configure AWS access, check `boto3 configuration`_ or export::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>


Configure the example route::

    Add to loafer/conf.py: LOAFER_ROUTES = [('a-queue-name', 'loafer.jobs.async_example_job')]
    | This will change soon!
 

.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
