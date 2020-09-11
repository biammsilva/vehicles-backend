FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

EXPOSE 8000 