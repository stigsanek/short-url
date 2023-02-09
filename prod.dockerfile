# syntax=docker/dockerfile:1

# creating a python base with shared environment variables
FROM python:3.8.16-slim-buster as base

# set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  POETRY_VERSION=1.2.2 \
  TEMP_DIR=/opt/tempdir \
  HOME=/home/app \
  APP_HOME=/home/app/web


# preparation stage of the requirements.txt file
FROM base as poetry

# install poetry
RUN pip install --upgrade pip && \
  pip install poetry==$POETRY_VERSION

# set work directory
WORKDIR $TEMP_DIR

# export to requirements.txt
COPY poetry.lock pyproject.toml $TEMP_DIR
RUN poetry export -f requirements.txt -o requirements.txt --only main


# final stage
FROM base as production

# create user and user directory
RUN mkdir -p $HOME \
  && mkdir $APP_HOME \
  && addgroup --system app \
  && adduser --system --group app

# set work directory
WORKDIR $APP_HOME

# install dependencies
COPY --from=poetry $TEMP_DIR/requirements.txt $APP_HOME/requirements.txt
RUN apt-get update && \
  apt-get -y install netcat && \
  pip install --upgrade pip && \
  pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
