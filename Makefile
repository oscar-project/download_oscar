# CLEAN
.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -rf lightning_logs
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +

# INSTALL
.PHONY: upgrade
upgrade:
	pip install --upgrade pip

.PHONY: install
install: clean upgrade
	pip install build wheel
	pip install .

.PHONY: packages
packages: clean upgrade
	pip install build wheel
	pip install -e .[dev]

.PHONY: develop
develop: packages
	pre-commit install

# BUILD
.PHONY: build
build: clean
	python -m build

# TEST
.PHONY: test
test:
	pytest --disable-warnings

.PHONY: coverage
coverage:
	pytest --disable-warnings --cov-report=xml --cov=.

# LINT
.PHONY: lint
lint:
	mypy download_oscar __tests__
	isort -c download_oscar __tests__
	pylint download_oscar __tests__
	flake8 download_oscar __tests__
	autoflake -c -r download_oscar __tests__

# FORMAT
.PHONY: black
black:
	black download_oscar __tests__

.PHONY: isort
isort:
	isort download_oscar __tests__

.PHONY: autoflake
autoflake:
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive download_oscar __tests__

.PHONY: format
format: clean black isort autoflake
