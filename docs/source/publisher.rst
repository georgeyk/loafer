Publisher
---------

The publisher is only used for testing purposes, so we can have an easy way
to validate some message translation process or handler execution.

It is responsible to publish a message in a provider source (queue).

It can be usefull to emulates the behavior of a given handler without the
real message producer.

At the moment we provide publishers for Amazon SQS and SNS. Check the
:doc:`quickstart/usage` for examples.
