# WARNING: `make` *requires* the use of tabs, not spaces, at the start of each command

PYTHON_INTERPRETER = python
PIP = pip

default: help

.PHONY: help
help: # help command
	@awk 'BEGIN {FS = ":.*#"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^#@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: install
install: # Install the project dependencies defined in the requirements.txt file.
	$(PIP) install -r requirements.txt

.PHONY: lint
lint: # Run linter, then exit with an error code if needed
	$(PYTHON_INTERPRETER) -m flake8 app/
	$(PYTHON_INTERPRETER) -m yapf --recursive --diff --parallel app

.PHONY: format
format: # Formats
	yapf --recursive --in-place --parallel --verbose app

.PHONY: test
test: # Run pytest
	pytest tests/test_main.py -vs

.PHONY: start
start: # Start application
	uvicorn app.main:app --reload

.PHONY: clean
clean: # remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

flag: # print the flag
	echo "bmljZSB0cnkhIFRoZSBmbGFnIGlzIG5vdCBoZXJl" | base64 --decode
