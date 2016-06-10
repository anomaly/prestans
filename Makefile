all: tests

tests:
	python -m unittest discover -s prestans

	