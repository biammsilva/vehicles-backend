
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

* Up the database:

        docker-compose up -d db

* Collect static files:

        python manage.py collectstatic --noinput

* Migrations:

        python manage.py migrate

### Run

    python manage.py runserver

`it will run at port 8000. You can set the port using python manage.py runserver 0.0.0.0:8001. Access the application with http://localhost:8000`

### Test
    
    python manage.py runserver

* Coverage:

        coverage run --source='.' manage.py test
        coverage report

`Note: Files as vehicles_backend/wsgi.py, vehicles_backend/asgi.py and manage.py will not have 100% of coverage because they are settings files`

## Run with docker:

* Pre requisites:

    * Docker;
    * Docker-compose;

### Setup

* Build application:

        docker-compose up --build

* Collect static files:

        docker-compose exec web python manage.py collectstatic

    `note: your container must be running to execute this command. You can do this by open another terminal or running the docker-compose in detached mode: docker-compose up -d`

* Migrations:

        docker-compose exec web python manage.py migrate

    `note: your container must be running to execute this command. You can do this by open another terminal or running the docker-compose in detached mode: docker-compose up -d`

### Run:

    docker-compose up -d

`it will run at port 8000. Access the application with` http://localhost:8000

### Test
    
    docker-compose exec web python manage.py runserver

* Coverage:

        docker-compose exec web coverage run --source='.' manage.py test
        docker-compose exec web coverage report

`Note: Files as vehicles_backend/wsgi.py, vehicles_backend/asgi.py and manage.py will not have 100% of coverage because they are settings files`

## Docs

Docs will be able at the application main page: http://localhost:8000

## Possible errors:

* `Port 8000 already in use`: 

    For that, kill the port and try again

        sudo lsof -t -i tcp:8000 | xargs sudo kill -9
