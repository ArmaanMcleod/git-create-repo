.PHONY: help
.PHONY: test
.PHONY: clean
.PHONY: install
.PHONY: sandbox
.PHONY: setup
.PHONY: upload
.PHONY: uninstall

help:
	@echo "Usage: make (rule)"
	@echo "Makefile rules:"
	@echo "test - Create test directory."
	@echo "clean - Clean extra directories generated."
	@echo "install - Install dependencies."
	@echo "sandbox - Install test pypi package."
	@echo "setup - Setup source distribution and wheel."
	@echo "upload - Upload source distribution and wheel to PyPi."
	@echo "uninstall - Uninstalls Pypi package."

test:
	mkdir test
	cp git_create.py test

clean:
	rm -rf test
	rm -rf build/
	rm -rf dist/
	rm -rf git_create_repo.egg-info

install:
	pip3 install -r requirements.txt

sandbox:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	pip3 install --extra-index-url https://testpypi.python.org/pypi git-create-repo

setup:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

upload:
	twine upload dist/*

uninstall:
	pip3 uninstall git-create-repo -y