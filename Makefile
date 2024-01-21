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
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
        . $(VENV_ACTIVATE) && pytest; \
    else \
        . $(VENV_ACTIVATE) && pytest tests/test_$(filter-out $@,$(MAKECMDGOALS)).py; \
    fi
%:
    @:

# Setup env for dev
dev: venv
	. $(VENV_ACTIVATE) && pre-commit autoupdate
	. $(VENV_ACTIVATE) && $(PIP) install -e .

# Run pre-commit
pcr:
	. $(VENV_ACTIVATE) && pre-commit run --all-files

# Build package
build:
	. $(VENV_ACTIVATE) && $(PYTHON) -m build
	. $(VENV_ACTIVATE) && $(PIP) install -e .

# Help
help:
	@echo "make - Run all tasks"
	@echo "make clean - Clean up the project"
	@echo "make venv - Set up the virtual environment"
	@echo "make test - Run tests with pytest"
	@echo "make dev - Setup a dev environment and installs the package locally"
	@echo "make pcr - Run pre-commit hooks"
	@echo "make build - Build the package"
