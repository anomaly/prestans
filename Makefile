.PHONY: test
test:
	python setup.py test

.PHONY: tests-prep
tests-prep:
	pip install tox tox-pyenv
	pyenv local 2.7.15 3.5.6 3.6.6 pypy2.7-6.0.0

.PHONY: tests
tests:
	tox

.PHONY: coverage
coverage:
	py.test --cov-report term-missing:skip-covered --cov-config .coveragerc --cov=prestans tests

.PHONY: dist
dist:
	if [ -a dist ]; then rm -rf dist/*; fi;
	python setup.py sdist bdist_wheel

.PHONY: release-test
release-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: release
release:
	twine upload dist/*

.PHONY: clean
clean:
	python setup.py clean
	if [ -a .cache ]; then rm -rf .cache; fi;
	if [ -a .pytest_cache ]; then rm -rf .pytest_cache; fi;
	if [ -a .eggs ]; then rm -rf .eggs; fi;
	if [ -a build ]; then rm -rf build; fi;
	if [ -a dist ]; then rm -rf dist; fi;
	if [ -a build ]; then rm -rf build; fi;
	if [ -a .tox ]; then rm -rf .tox; fi;
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +