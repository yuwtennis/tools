FROM python:3.10-alpine

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.5.1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN python3 -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION

WORKDIR /app
ADD . /app
RUN $POETRY_HOME/bin/poetry install