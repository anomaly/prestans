test:
	echo "Running all tests ..."
	python -m unittest discover -s prestans


publish:
	python setup.py sdist bdist_wheel upload	
