# django-planetarium-api
planetarium api

## Description

Django CRUD API 
- The goal of this exercise is to retrieve data from an external source, store it in an  appropriate database structure, and create a CRUD RESTful API to interface with the database.
- Goals 
    - Read the data from this endpoint: https://swapi-graphql.netlify.app/.netlify/functions/index?query=query%20Query%20{allPlanets{planets{name%20population%20terrains%20climates}}}
    - Store the data from the endpoint into the database and create appropriate models 
    - Write RESTful Create, Read, Update, and Delete endpoints to interact with the database

## Authors and acknowledgment
Ana M. Rodriguez Hernandez
planetarium api is an assessment of Django CRUD Api

## License
For open source projects, say how it is licensed.

# local setup
* create virtual venv: `virtualenv -p /usr/local/bin/python3.12 venv`
* activate: `source venv/bin/activate`
* install dependencies: `pip install -r requirements.frozen`
* run server: `python manage.py runserver`
    * admin UI: http://127.0.0.1:8000/admin/ 
* run init migration: `python manage.py migrate`
* create super user: `python manage.py createsuperuser`
*    super user for this assessment: admin:admin
* create migrations based on models
    * `python manage.py makemigrations`
    * run migrations: `python manage.py migrate`
* run test
    * `./manage.py test`

More helper commands
* install pip-tool: `pip install pip-tools`
* get dependencies: `pip freeze`
* project user flake8 for lint configurations are in `setup.cfg`
    * run lint: `flake8`


* planet list for testing: https://dragonball.fandom.com/wiki/List_of_Planets

