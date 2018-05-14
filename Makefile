clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

install:
	python setup.py install