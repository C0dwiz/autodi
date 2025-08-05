.DEFAULT_GOAL := lint

# Project folders
package_dir := autodi
tests_dir := tests
code_dirs := $(package_dir) $(tests_dir)

# =================================================================================================
# Environment
# =================================================================================================

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -rf *.egg-info
	rm -f report.html
	rm -f .coverage
	rm -rf {build,dist,site,.cache,.hypothesis,.mypy_cache,.ruff_cache,reports,htmlcov}

.PHONY: install
install:
	poetry install --no-root
	poetry run pre-commit install

# =================================================================================================
# Code Quality
# =================================================================================================

.PHONY: lint
lint:
	poetry run black --check --diff $(code_dirs)
	poetry run isort --check-only $(code_dirs)
	poetry run ruff check $(code_dirs)

.PHONY: type-check
type-check:
	poetry run mypy $(package_dir)

.PHONY: format
format:
	poetry run black $(code_dirs)
	poetry run isort $(code_dirs)

.PHONY: check
check: lint type-check test

# =================================================================================================
# Tests
# =================================================================================================

.PHONY: test
test:
	poetry run pytest $(tests_dir)
