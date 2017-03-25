Managers
--------

Managers are responsible for the execution of all the components.

The ``LoaferManager`` (at ``loafer.managers``) receives a ``list`` of :doc:`routes`.

Every service/application using ``loafer`` should instantiate a manager::

    from loafer.managers import LoaferManager
    from .routes import routes  # the list of routes

    manager = LoaferManager(routes=routes)
    manager.run()


The default execution mode will run indefinitely.
To run only one iteration of your services, the last line in the code above
should be replaced with::

    manager.run(forever=False)


The "one iteration" could be a little tricky. For example, if you have one
provider that fetches two messages at time, it means your handler will be called
twice (one for each message) and then stop.
