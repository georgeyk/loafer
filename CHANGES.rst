1.2.0 (2017-08-15)
------------------

* Enable provider parameters (boto client options)

1.1.1 (2017-06-14)
------------------

* Bugfix: fix SNS prefix value in use for topic name wildcard (by @lamenezes)

1.1.0 (2017-05-01)
------------------

* Added initial contracsts for class-based handlers
* Added generic handlers: SQSHandler/SNSHander
* Improve internal error handling
* Improve docs

1.0.2 (2017-04-13)
------------------

* Fix sentry error handler integration

1.0.1 (2017-04-09)
------------------

* Add tox and execute tests for py36
* Update aiohttp/aiobotocore versions
* Minor fixes and enhancements


1.0.0 (2017-03-27)
------------------

* Major code rewrite
* Remove CLI
* Add better support for error handlers, including sentry/raven
* Refactor exceptions
* Add message metadata information
* Update message lifecycle with handler/error handler return value
* Enable execution of one service iteration (by default, it still runs "forever")


0.0.3 (2016-04-24)
------------------

* Improve documentation
* Improve package metadata and dependencies
* Add loafer.aws.message_translator.SNSMessageTranslator class
* Fix ImportError exceptions for configuration that uses loafer.utils.import_callable


0.0.2 (2016-04-18)
------------------

* Fix build hardcoding tests dependencies


0.0.1 (2016-04-18)
------------------

* Initial release
