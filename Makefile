# Makefile

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docs

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr deployments/build/
	rm -fr deployments/Dockerfiles/open_aea/packages
	rm -fr pip-wheel-metadata
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	find . -name '*.svn' -exec rm -fr {} +
	find . -name '*.db' -exec rm -fr {} +
	rm -fr .idea .history
	rm -fr venv

.PHONY: clean-docs
clean-docs:
	rm -fr site/

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.DS_Store' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -f .coverage
	find . -name ".coverage*" -not -name ".coveragerc" -exec rm -fr "{}" \;
	rm -fr coverage.xml
	rm -fr htmlcov/
	rm -fr .hypothesis
	rm -fr .pytest_cache
	rm -fr .mypy_cache/
	find . -name 'log.txt' -exec rm -fr {} +
	find . -name 'log.*.txt' -exec rm -fr {} +

.PHONY: hashes
hashes: clean fmt lint
	poetry run autonomy packages lock
	git add packages
	git commit -m 'chore: hashes'

lint:
	poetry run adev -v -n 0 lint

fmt: 
	poetry run adev -n 0 fmt

test:
	poetry run adev test

all: fmt lint test hashes

install: update_git_deps
	poetry install
	poetry run autonomy packages sync



update_git_deps:
	if [ ! -d "third_party/upstream" ]; then \
		echo "The third-party dependencies are not visible. Please run 'git submodule update --init --recursive'"; \
		git submodule update --init --recursive;fi


is_dirty:
	# Check if the repository is dirty.
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "The repository is dirty. Please commit your changes first."; \
		exit 1; \
	fi
