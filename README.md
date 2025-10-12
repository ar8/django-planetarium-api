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
* run init migration: `python manage.py migrate`
* create super user: `python manage.py createsuperuser`
*    super user for this assessment: admin:admin
* create migrations based on models
    * `python manage.py makemigrations`
    * run migrations: `python manage.py migrate`
* create seeds for  terrains & climates
    * `python manage.py seed_data`
* run server: `python manage.py runserver`
    * admin UI: http://127.0.0.1:8000/admin/
* tox is used run test
    * `tox`

More helper commands
* install pip-tool: `pip install pip-tools`
* get dependencies: `pip freeze`
* project user flake8 for lint configurations are in `setup.cfg`
    * run lint: `flake8`


* planet list for testing: https://dragonball.fandom.com/wiki/List_of_Planets

## Testing Notes
* Postman collection is in /Planetarium.postman_collection.json
* For testing purpose I created a variable in settings.py > PLANETS_AUTH_REQUIRED = False to avoid the tedious process of get the bearer token and set it up
* For testing with security you need to:
    * In settings.py set PLANETS_AUTH_REQUIRED = True
    * Add authorization => Auth Type: Bearer Token, Token: {{BEARER_TOKEN}}
    * Run endpoint get_bearer_token to get the value anc copy value of "access" to collection variable BEARER_TOKEN
* Rules: 
    * You need to add a `Terrain` to the database before use it
        * Available values are: Rocky ,Ocean ,Desert ,Grasslands ,Mountains ,Plains ,Lakes ,Islands
        * Add one in: http://127.0.0.1:8000/admin/planets/terrain/
    * You need to add a `Climate` to the database before use it
        * Available values are: Tropical ,Arid ,Temperate ,Mild ,Humid
        * Add one in:  http://127.0.0.1:8000/admin/planets/climate/

## Documentation
- Docs: http://127.0.0.1:8000/api/docs/


