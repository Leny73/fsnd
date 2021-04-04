import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth



app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

## ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    short_drinks = [drink.short() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": short_drinks
    }), 200

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    drinks = Drink.query.order_by(Drink.id).all()
    long_drinks = [drink.long() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": long_drinks
    }), 200

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    body = request.get_json()
    new_title = request.json.get("title")
    new_recipe = request.json.get("recipe")
    try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()

        drinks = Drink.query.order_by(Drink.id).all()
        long_drinks = [drink.long() for drink in drinks]

        return jsonify({
            "success": True,
            "drinks": long_drinks
        }), 200
    except Exception as e: 
        print(e)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)
        
        new_title = request.json.get("title")
        new_recipe = request.json.get("recipe")
        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)
        drink.update()
        drinks = Drink.query.order_by(Drink.id).all()
        long_drinks = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": long_drinks
        }), 200
    except Exception as e: 
        print(e)



@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource not found!"
        }), 404

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