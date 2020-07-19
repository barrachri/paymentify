build:
	docker build -t paymentify .

run-container: build
	docker run --rm -p 8888:8888 paymentify

test:
	poetry run pytest -v

run:
	poetry run gunicorn paymentify.main:api
