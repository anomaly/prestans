test:
	echo "Running all tests ..."
	python setup.py test

build:
	python setup.py sdist bdist_wheel

publish:
	python setup.py sdist bdist_wheel upload

clean:
	python setup.py clean --all