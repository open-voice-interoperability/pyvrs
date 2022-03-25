.PHONY: usage dev

usage:
	@echo "usage: make [dev]"

dev: requirements.txt
	pip3 install -r requirements.txt
	pip install --editable .
