FROM python:3.11-slim-bullseye

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE="false"

RUN python3 -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION

WORKDIR /app
ADD . ./
RUN $POETRY_HOME/bin/poetry install