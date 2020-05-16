Loafer
======

|PyPI latest| |PyPI Version| |PyPI License| |Docs|

|CI Build Status| |Coverage Status| |Requirements Status|
|Scrutinizer Code Quality| |Code Climate|

----

Loafer is an asynchronous message dispatcher for concurrent tasks processing.

**Currently, only AWS SQS is supported**


Features:

* Encourages decoupling from message providers and consumers
* Easy to extend and customize
* Easy error handling, including integration with sentry
* Easy to create one or multiple services
* Generic Handlers
* Amazon SQS integration


It requires Python 3.6+ and is very experimental at the moment, expect a lot
of changes until the first major version.


Example
~~~~~~~

A simple message forwader, from ``source-queue`` to ``destination-queue``:

.. code:: python

    from loafer.ext.aws.handlers import SQSHandler
    from loafer.ext.aws.routes import SQSRoute
    from loafer.managers import LoaferManager


    routes = [
        SQSRoute('source-queue', handler=SQSHandler('destination-queue')),
    ]


    if __name__ == '__main__':
        manager = LoaferManager(routes)
        manager.run()


Documentation
~~~~~~~~~~~~~

Check out the latest **Loafer** full documentation at `Read the Docs`_ website.


.. _`Read the Docs`: http://loafer.readthedocs.org/



.. |Docs| image:: https://readthedocs.org/projects/loafer/badge/?version=latest
   :target: http://loafer.readthedocs.org/en/latest/?badge=latest
.. |CI Build Status| image:: https://circleci.com/gh/georgeyk/loafer.svg?style=svg
   :target: https://circleci.com/gh/georgeyk/loafer
.. |Coverage Status| image:: https://codecov.io/gh/georgeyk/loafer/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/georgeyk/loafer
.. |Requirements Status| image:: https://requires.io/github/georgeyk/loafer/requirements.svg?branch=master
   :target: https://requires.io/github/georgeyk/loafer/requirements/?branch=master
.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/georgeyk/loafer/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/georgeyk/loafer/?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/georgeyk/loafer/badges/gpa.svg
   :target: https://codeclimate.com/github/georgeyk/loafer
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/loafer.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/loafer
.. |PyPI License| image:: https://img.shields.io/pypi/l/loafer.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/loafer
.. |PyPI latest| image:: https://img.shields.io/pypi/v/loafer.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/loafer
