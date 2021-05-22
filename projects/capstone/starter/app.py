import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Location, Event
from flask_cors import CORS
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
  @app.route('/')
  def get_greeting():
    # excited = os.environ['EXCITED']
    greeting = "Hello !!!" 
    return greeting

  @app.route('/locations', methods=['GET'])
  @requires_auth('get:locations')
  def locations(jwt):
      locations = Location.query.order_by(Location.id).all()
      data = []
      for location in locations:
        data.append({
          "id": location.id,
          "name": location.name,
          "location": location.location
        })

      if len(locations) == 0:
          abort(404)
      else:
          format_locations = [location.format() for location in locations]

          return jsonify({
              'success': True,
              'locations': format_locations,    
              'total_locations': len(format_locations),
          })

  @app.route('/locations', methods=['POST'])
  @requires_auth('post:locations')
  def add_location(jwt):
      body = request.get_json()
      new_name = body.get('name', None)
      new_location = body.get('location', None)

      try:
        location = Location(name=new_name, location=new_location)
        print(location)
        location.insert()

        return jsonify({
            'success': True,
        })
      except Exception as e: 
        print(e)

  @app.route('/events', methods=['GET'])
  @requires_auth('get:events')
  def events(jwt):
      events = Event.query.order_by(Event.id).all()
      data = []
      for event in events:
        data.append({
          "id": event.id,
          "name": event.name,
          "location": event.location
        })

      if len(events) == 0:
          abort(404)
      else:
          formatted_events = [event.format() for event in events]
          return jsonify({
              'success': True,
              'events': formatted_events,
              'data': data,
              'total_events': len(formatted_events),
          })
  
  @app.route('/events', methods=['POST'])
  @requires_auth('post:events')
  def add_event(jwt):
      body = request.get_json()
      new_name = body.get('name', None)
      new_location = body.get('location', None)

      try:
        event = Event(name=new_name, location=new_location)
        print(event)
        event.insert()

        return jsonify({
            'success': True,
        })
      except Exception as e: 
        print(e)


  @app.route('/events/<int:id>', methods=['PATCH'])
  @requires_auth('patch:events')
  def update_event(jwt, id):
      try:
          event = Event.query.filter(Event.id == id).one_or_none()

          if event is None:
              abort(404)
          
          new_name = request.json.get("name")
          new_location = request.json.get("location")
          event.name = new_name
          event.location = new_location
          event.update()
          events = Event.query.order_by(Event.id).all()
          events_formatted = [event.format() for event in events]

          return jsonify({
              "success": True,
              "events": events_formatted
          }), 200
      except Exception as e: 
          print(e)

  @app.route('/events/<int:id>', methods=['DELETE'])
  @requires_auth('delete:events')
  def delete_event(jwt, id):
    try:
        event = Event.query.filter(Event.id == id).one_or_none()

        if event is None:
            abort(404)

        event.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)
  
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource not found!"
            }), 404

  @app.errorhandler(422)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable!"
            }), 422

  @app.errorhandler(400)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request!"
            }), 400

  @app.errorhandler(405)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed!"
            }), 405

  @app.errorhandler(AuthError)
  def auth_error(e):
    print(e)
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), e.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    