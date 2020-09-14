
# Vehicles localization API

API to provide data for vehicles localization.

## Technologies choice:

### Django:

Django rest framework has scaffolds and builtins resources that allows to create a CRUD easily than another frameworks. The viewsets and the orm helps a lot to create a simple API.

## Postgres:

I've choosen PostgreSQL because of his postgis extension, that would allow the scale of the project, working with geo referenced querying in database.

## Solution choices:

The endpoint GET http://api-url/vehicles used to be a return a full list of the vehicles and its locations.
But, optimizing the apllication, I've choosen to return only the vehicles that had at least one location and show only the last location of the vehicle.
That way, it could be showed on the map, and if the user wants to see the locations of the vehicle, the endpoint GET http://api-url/vehicles/id-vehicle/locations can be requested and return all the locations of that specific vehicle.
If you want to see all the vehicles use the queryparam 'all': http://api-url/vehicles?all=1

When a location is added, the software verify if the geopoint is inside the 3.5km radious from door2door office. If it's not, the API return a 400 status code and the message: "Location out of the city boundaries".

**Production url**: https://api-vehicles.herokuapp.com/

In that link, you can see the endpoint documented

### Solution in 1000+ vehicles case:

For that I would deploy the api in a serverless resource, such as: Lambda, Cloud functions, Azure Functions...
That way, the serverless application would handle the scale as it occours.

One thing that I've made to help with that in the backend, was to show at /vehicles endpoint only the last position of the vehicle, so, the payload would not be do heavy.
And in the frontend, I've clusterized the map, to get the visualization easier.

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
