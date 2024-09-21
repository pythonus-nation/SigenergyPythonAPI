all:
	install-dev

install-dev:
	pip3 install -r requirements.txt

clean:
	rm -rf dist/*


build:
	python3 -m build

upload:
	python3 -m twine upload dist/*

install:
	python3 -m pip install SigenAPI


upload-test:
	python3 -m twine upload --repository testpypi dist/*

install-test:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps sigenapi_pythonus-nation
