Development Installation
========================

Requirements
------------

Python 3.5+

Note::

    Some packages also needs python3.5-dev package (ubuntu) or similar


Development install
-------------------

After forking or checking out::

    $ cd loafer/
    $ python setup.py develop
    $ pip install -r requirements/local.txt
    $ pre-commit install


The requirements folder are only used for development, so we can easily
install/track dependencies required to run the tests using continuous
integration platforms.

The official entrypoint for distritubution is the ``setup.py`` which also
contains the minimum requirements to execute the tests.

It's important to execute ``setup.py develop`` not only to install the main
dependencies, but also to include ``loafer`` CLI in our environment.


Running tests::

    $ make test

Generating documentation::

    $ cd docs/
    $ make html


To configure AWS access, check `boto3 configuration`_ or export  (see `boto3 envvars`_)::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>
    $ export AWS_DEFAULT_REGION=sa-east-1  # for example


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
.. _boto3 envvars: http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variable-configuration

Check the :doc:`../settings` section to see specific configurations.
