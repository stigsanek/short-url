# syntax=docker/dockerfile:1
FROM python:3.8.16-slim-buster

# set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  POETRY_VERSION=1.2.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  APP_HOME=/app

# install dependencies
RUN apt-get update && \
  apt-get -y install netcat && \
  pip install --upgrade pip && \
  pip install poetry==$POETRY_VERSION

# set work directory
WORKDIR $APP_HOME

# install python dependencies
COPY poetry.lock pyproject.toml $APP_HOME
RUN poetry install --no-root

# copy project
COPY . $APP_HOME

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
