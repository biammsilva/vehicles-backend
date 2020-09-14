FROM python:3.6-slim

ARG db_host=db

ENV PIP_NO_CACHE_DIR=1 \
DB_HOST=${db_host}

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000 