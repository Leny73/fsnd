# Brother Map - Capstone 
This is an application to showcase all the events and locations connected with the White Brotherhood in Bulgaria. It will be integrated with a Map to showcase all
of the events that are going to be held and all sacred locations in Bulgaria where the Master Petar Deunoff was travelling and visiting specific areas.

## Instructions

## Getting Started

### Installing Dependencies

#### PIP Dependencies

Install dependencies by naviging to the `/starter` directory and running:

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


### API

#### Error Types
The API will retern three error types when requests fail:
* 400: Bad Request!
* 404 Resource Not Found
* 422 Not Processable
* 405 Method Not Allowed
* 401 Unauthorized

#### Endpoints

##### GET /events
- Returns a list of event objects, value of success and a total number of event
* Sample : In terminal with curl installe type: <code>curl https://brothermap.herokuapp.com/events -H "Content-Type: application/json, 'Authorization': Event_Manager_jwt"</code>
* Sample Response : <code>
  {
    "data": [
        {
            "id": 1,
            "location": "event",
            "name": "event"
        }
    ],
    "events": [
        {
            "id": 1,
            "location": "event",
            "name": "event"
        }
    ],
    "success": true,
    "total_events": 1
}
</code>

##### POST /events
- Creates a new event using the submitted title and location. Return success value.
* Example: <code> curl https://brothermap.herokuapp.com/events -X POST -H "Content-Type: application/json, 'Authorization': Event_Manager_jwt" -d '{"name":"Masons", "location":"Jean Palu"}'</code>
* Example response: <code>
  {
    "success": true
}
</code>

##### DELETE /events/{book_id}
- Deletes a selected event id. Returns event id, success value.
* Example: <code> curl -X DELETE https://brothermap.herokuapp.com/events/1 -H "Content-Type: application/json, 'Authorization': Event_Manager_jwt"</code>
* Example Response: <code> 
  {
    "delete": 1,
    "success": true
}
</code>

##### PATCH /events/{event_id}
- If provided, updates rating of the specific event_id. Return all events.
* Example: <code> curl -X PATCH https://brothermap.herokuapp.com/events1 -H "Content-Type: application/json, 'Authorization': Event_Manager_jwt" -d '{"name":"newEventPatched","location":"newLocationsPatched"}'
* Example Response: <code>
  {
    "events": [
        {
            "id": 1,
            "location": "newLocationsPatched",
            "name": "newEventPatched"
        },
        {
            "id": 2,
            "location": null,
            "name": "newEvent"
        }
    ],
    "success": true
}
  </code>
##### GET /locations
- Returns a list of locations objects, value of success and a total number of locations
* Sample : In terminal with curl installe type: <code>curl https://brothermap.herokuapp.com/locations -H "Content-Type: application/json, 'Authorization': Locations_Manager_jwt"</code>
* Sample Response : <code>
  {
    "locations": [
        {
            "id": 1,
            "location": "Location",
            "name": "Location Name"
        }
    ],
    "success": true,
    "total_events": 1
}
</code>

##### POST /Locations
- Creates a new location using the submitted title and location. Return success value.
* Example: <code> curl https://brothermap.herokuapp.com/locations -X POST -H "Content-Type: application/json, 'Authorization': Location_Manager_jwt" -d '{"name":"Location Other", "location":"Timboktu"}'</code>
* Example response: <code>
  {
    "success": true
}
</code>

  
 
