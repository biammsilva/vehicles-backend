
# Vehicles localization API

API to provide data for vehicles localization.

## Run with virtual environment:

### Setup

* Pre requisites:

    * Pip
    * Pipenv
    * Python3.6

`note: to install pipenv globally use: sudo -H pip install -U pipenv`

* Activate virtual environment:

        pipenv shell

* Install Dependencies:

        pipenv install

* Collect static files:

        python manage.py collectstatic --noinput

* Migrations:

        python manage.py migrate

### Run

    python manage.py runserver

`it will run at port 8000. You can set the port using python manage.py runserver 0.0.0.0:8001. Access the application with http://localhost:8000`

## Docs

Docs will be run at the application main page: http://localhost:8000

## Run with docker:

* Pre requisites:

    * Docker;
    * Docker-compose;

### Setup

* Build application:

        docker-compose up --build

* Collect static files:

        docker-compose exec web python manage.py collectstatic

    `note: your container must be running to execute this command. You can do this by open another terminal or running the docker-compose in the daemon mode: docker-compose up -d`

* Migrations:

        docker-compose exec web python manage.py migrate

    `note: your container must be running to execute this command. You can do this by open another terminal or running the docker-compose in the daemon mode: docker-compose up -d`

### Run:

    docker-compose up -d

`it will run at port 8000. Access the application with http://localhost:8000`

## Possible errors:

* `Port 8000 already in use`: 

    For that, kill the port and try again

        sudo lsof -t -i tcp:8000 | xargs sudo kill -9
