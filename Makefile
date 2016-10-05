test:
	echo "Running all tests ..."
	python setup.py test


publish:
	python setup.py sdist bdist_wheel upload	
