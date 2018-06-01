clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

install:
	python setup.py install

test:
	python -m unittest discover -s tests/ -p "*_test.py" -v

lint:
	pylint --load-plugins pylint_quotes aperture/

