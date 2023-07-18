SHELL = /usr/bin/env bash -xeuo pipefail

isort:
	poetry run isort src/

black:
	poetry run black src/

format: isort black

.PHONY: \
	isort \
	black \
	format
