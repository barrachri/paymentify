# Paymentify
![Test & Linters & Deploy](https://github.com/barrachri/paymentify/workflows/Test%20&%20Linters%20&%20Deploy/badge.svg)
[![codecov](https://codecov.io/gh/barrachri/paymentify/branch/master/graph/badge.svg)](https://codecov.io/gh/barrachri/paymentify)

## How to start

With `poetry` available on your path

```
poetry install
```

## How to run test
```
make test
```
or

```
poetry run pytest
```

## How to run paymentify
```
make run
```
or
```
poetry run gunicorn paymentify.main:api
```
or inside a container

```
make run-container
```

## How to develop locally
We use [pre-commit](https://pre-commit.com/) to run linters and checks on each commit.

After you run `poetry install` you can run `poetry run pre-commit install` to install the git hook.

## Endpoints

- `/tokenise` (tokenise a card)
- `/sale` (charge a card)
- `/health` (healthcheck for the APIs)
