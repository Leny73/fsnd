# Brother Map - Capstone 
This is an application to showcase all the events and locations connected with the White Brotherhood in Bulgaria. It will be integrated with a Map to showcase all
of the events that are going to be held and all sacred locations in Bulgaria where the Master Petar Deunoff was travelling and visiting specific areas.

## Instructions

## Getting Started

### Installing Dependencies

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
or pip3 depending on python installation

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.


## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Setup Auth0

I have set up 2 roles Locations Manager and Event Manager that have specific permissions in the app to make requests
without these permissions you wouldn't be able to make requests to the application.

AUTH0_DOMAIN = 'twbm.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
CLIENT_ID = 'aGu0hcE53n4V0YLEn7cIG8PAs0dBJiiy'
CALLBACK_URL = 'https://brothermap.herokuapp.com/'

Using https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

This will generate an API token which can be used based on permissions to make requests via curl or postman.

### Unit Tests

There are unit tests to check all endpoints and see if endpoints are returning the corrects values

run `python3 test_app.py` command to check results

### Postman Tests

I included Postman tests to check locally how my application works as it was easier to debug.








