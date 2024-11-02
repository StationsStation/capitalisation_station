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
hashes: clean
	poetry run autonomy packages lock
	poetry run autonomy push-all

lint:
	poetry run adev -v -n 0 lint

fmt: 
	poetry run adev -n 0 fmt

test:
	poetry run adev -v test

install:
	bash install.sh
	poetry run autonomy packages sync

 sync:
	git pull
	poetry run autonomy packages sync

all: fmt lint test hashes


metadata:
	# pending updates.
	# poetry run adev metadata generate . protocol/eightballer/balances/0.1.0 06 && adev -v metadata validate mints/06.json
	# poetry run adev metadata generate . protocol/eightballer/markets/0.1.0 07 && adev -v metadata validate mints/07.json
	# poetry run adev metadata generate . protocol/eightballer/ohlcv/0.1.0 08 && adev -v metadata validate mints/08.json
	# poetry run adev metadata generate . protocol/eightballer/orders/0.1.0 09 && adev -v metadata validate mints/09.json
	# poetry run adev metadata generate . protocol/eightballer/positions/0.1.0 10 && adev -v metadata validate mints/10.json
	# poetry run adev metadata generate . protocol/eightballer/spot_asset/0.1.0 11 && adev -v metadata validate mints/11.json
	# poetry run adev metadata generate . protocol/eightballer/tickers/0.1.0 12 && adev -v metadata validate mints/12.json

	# minted.
	# poetry run adev metadata generate . protocol/eightballer/order_book/0.1.0 13 && adev -v metadata validate mints/13.json
	# poetry run adev metadata generate . contract/eightballer/spl_token/0.1.0 14 && adev -v metadata validate mints/14.json
	# poetry run adev metadata generate . contract/vybe/jupitar_swap/0.1.0 15 && adev -v metadata validate mints/15.json
	# poetry run adev metadata generate . connection/eightballer/dcxt/0.1.0 16 && adev -v metadata validate mints/16.json
	# poetry run adev metadata generate . connection/eightballer/ccxt/0.1.0 17 && adev -v metadata validate mints/17.json

	# poetry run adev metadata generate . custom/eightballer/arbitrage_strategy/0.1.0 18 && adev -v metadata validate mints/18.json
	# poetry run adev metadata generate . skill/eightballer/simple_fsm/0.1.0 19 && adev -v metadata validate mints/19.json

	poetry run adev metadata generate . agent/eightballer/trader/0.1.0 20 && adev -v metadata validate mints/20.json
	poetry run adev metadata generate . service/eightballer/cex_dex_arbitrage/0.1.0 21 && adev -v metadata validate mints/21.json