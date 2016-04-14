.PHONY: clean-pyc

clean-pyc:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@find . -iname '.coverage' -delete

clean: clean-pyc

test:
	py.test -vv

test-cov:
	py.test -vv --cov=loafer

cov:
	coverage report -m

cov-report:
	py.test -vv --cov=loafer --cov-report=html
