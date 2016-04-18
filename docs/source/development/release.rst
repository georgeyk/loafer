Release
-------

To release a new version, a few steps are required:

1. Update version number at ``loafer/__init__.py``

2. Add entry to ``CHANGES.rst`` and documentation

3. Test with ``python setup.py test`` and ``make test-cov``

4. Test build with ``make dist``

5. Commit changes

6. Release with ``make release``
