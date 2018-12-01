.PHONY: help
.PHONY: test
.PHONY: clean
.PHONY: install
.PHONY: setup
.PHONY: upload

help:
	@echo "Usage: make (rule)"
	@echo "Makefile rules:"
	@echo "test - Create test directory."
	@echo "clean - Clean extra directories generated."
	@echo "install - Install dependencies."
	@echo "setup - Setup source distribution and wheel."
	@echo "upload - Upload source distribution and wheel to PyPi."

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

setup:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

upload:
	twine upload dist/*