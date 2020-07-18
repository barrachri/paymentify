FROM python:3.7.7-slim-buster

ENV PATH="/root/.poetry/bin:$PATH"
ENV TINI_VERSION="v0.18.0"
ENV POETRY_VERSION="1.0.9"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PORT=8888

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN useradd -m -r user && \
    mkdir /src && \
    chown user /src

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends \
    wget \
    && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel && \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python get-poetry.py --version ${POETRY_VERSION} --yes && \
    # install deps globally
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /src/
WORKDIR /src
RUN poetry install --no-dev

COPY . /src

ENTRYPOINT ["/tini", "--"]
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 paymentify.main:api
