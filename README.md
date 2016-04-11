# loafer

Asynchronous Queue Consumer

It uses Amazon SQS and asyncio library.


** REALLY EXPERIMENTAL - CONCEPT-PROOF**


### Requirements

Python 3.5+
> Some packages also needs python3.5-dev package (ubuntu) or similar

Other requirements could be found at requirements folder in the project tree.


### Development install

After forking or checking out:

```
$ cd loafer/
$ pip install -r requirements.txt
$ pip install -r requirements/local.txt
```

* Configuring AWS access, check [boto3 configuration][boto3] or export:

```
$ export AWS_ACCESS_KEY_ID=<key>
$ export AWS_SECRET_ACCESS_KEY=<secret>
```

* Configure the example route:

Add to loafer/conf.py: LOAFER_ROUTES = [('a-queue-name', 'loafer.jobs.async_example_job')]
> This will change soon!


### Examples

* Starting loafer:

```
$ loafer
```

* Publishing a message to SNS/SQS (you should see some logging messages):

```
# To SQS
$ loafer publish --queue a-queue-name --msg 'foobar'

# To SNS (considering, the queue we consume are subscribed to topic)
$ loafer publish --topic a-topic-name --msg 'foobar'
```

[boto3]: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
