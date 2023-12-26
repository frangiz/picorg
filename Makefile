# Project variables
PROJECT_NAME := picorg
PYTHON := python3
PIP := pip3

# Virtual Environment
VENV := .venv
VENV_ACTIVATE := $(VENV)/bin/activate

.PHONY: all clean test build venv

# Default target
all: clean venv test build

# Clean up
clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf $(VENV)
	rm -rf build/
	rm -rf dist/
	rm -rf src/*.egg-info
	rm -rf .pytest_cache/
	rm -rf tests/working_dir/
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type f -name '.coverage' -delete
	find . -type f -name 'coverage.xml' -delete

# Create virtual environment
venv:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	. $(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt

# Run tests
test:
	. $(VENV_ACTIVATE) && pytest

# Setup env for dev
dev: venv
	. $(VENV_ACTIVATE) && $(PIP) install -e .

# Run pre-commit
pcr:
	pre-commit run --all-files --show-diff-on-failure

# Build package
build: test
	. $(VENV_ACTIVATE) && $(PYTHON) -m build
	. $(VENV_ACTIVATE) && $(PIP) install -e .

# Help
help:
	@echo "make - Run all tasks"
	@echo "make clean - Clean up the project"
	@echo "make venv - Set up the virtual environment"
	@echo "make test - Run tests with pytest"
	@echo "make build - Build the package"
