Release
-------

To release a new version, a few steps are required:

* Update version number at ``loafer/__init__.py`` and ``docs/source/conf.py``

* Add entry to ``CHANGES.rst`` and documentation

* Review changes in test requirements (``requirements/test.txt`` and ``setup.py``)

* Test with ``python setup.py test`` and ``make test-cov``

* Test build with ``make dist``

* Commit changes

* Release with ``make release``
