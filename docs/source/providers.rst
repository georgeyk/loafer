Providers
---------

Providers are responsible to retrieve messages and acknowledge it
(delete from source).


SQSProvider
~~~~~~~~~~~


``SQSProvider`` (located at ``loafer.ext.aws.providers``) receives the following options:

    * ``queue_name``: the queue name
    * ``endpoint_url`` (optional): the base url, only usefull if you don't use AWS
    * ``use_ssl`` (optional, default=True): SSL usage
    * ``options``: (optional): a ``dict`` with SQS options to retrieve messages.
      Example: ``{'WaitTimeSeconds: 5, 'MaxNumberOfMessages': 5}``


Usually, the provider are not configured manually, but set by :doc:`routes` and
it's helper classes.
