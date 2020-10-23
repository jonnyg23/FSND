import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# '''

# db_drop_and_create_all()

# ROUTES
# '''
# COMPLETED
# @TODO implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks}
#         where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''


@app.route('/drinks', methods=['GET'])
def retrieve_drinks():
    """
    GET request to retrieve drinks from database.
    --------------------
    Tested with:
        - Auth0 'GET /drinks'
    """
    try:
        # Query the database and order drinks by ids
        selection = Drink.query.order_by(Drink.id).all()
        drinks = []
        # Could use list comprehension
        for drink in selection:
            drinks.append(drink.short())

        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        # Print exception error as well as abort 500
        print(f'Exception "{e}" in retrieve_drinks()')
        abort(500)


# '''
# COMPLETED
# @TODO implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks}
#         where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(payload):
    """
    GET request to retrieve drink details from database.
    --------------------
    Tested with:
        - Auth0 GET /drinks-detail
    """
    try:
        # Query the database and order drinks by ids
        selection = Drink.query.order_by(Drink.id).all()
        drinks = []
        # Could use list comprehension
        for drink in selection:
            drinks.append(drink.long())

        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        # Print exception error as well as abort 500
        print(f'Exception "{e}" in retrieve_drinks_detail()')
        abort(500)


# '''
# COMPLETED
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink}
#     where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    """
    POST request to add a new drink to the database.
    --------------------
    Tested with:
        - Auth0 'POST /drinks'
    """
    # Retrieve the json body
    body = request.get_json()

    # If invalid json body, abort
    if not body:
        abort(400)

    # Get parameters from body
    title = body.get('title', None)
    # recipe = body.get('recipe', None)

    # Used code review suggestion below
    if type(body.get('recipe')) == str:
        recipe = body.get('recipe')
    else:
        recipe = json.dumps(body.get('recipe'))
    
    try:

        # Create a new drink, using body as inputs
        drink = Drink(
            title=title,
            recipe=recipe
        )
        # Insert into database
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception as e:
        # Print exception error and rollback database
        print(f'Exception "{e}" in create_drink()')
        db.session.rollback()


# '''
# COMPLETED
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink}
#     where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, id):
    """
    PATCH request to edit drink in the database.
    --------------------
    Tested with:
        - Auth0 'PATCH /drinks/<id>'
    """
    # Query database for the selected id
    drink_selected = Drink.query.filter(
        Drink.id == id).one_or_none()

    if not drink_selected:
        # If drink not found in database with id, abort 404
        abort(404)

    # Get parameters from body
    body = request.get_json()

    # If invalid json body, abort
    if not body:
        abort(400)

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    try:
        # If title or recipe is present, then update each correspondingly
        if title:
            drink_selected.title = title
        # if recipe:
        #     drink_selected.recipe = json.dumps(recipe)

        # Used code review suggestion below
        if type(recipe) == str:
            drink_selected.recipe = recipe
        else:
            drink_selected.recipe = json.dumps(recipe)

        # Update database session (runs db.session.commit())
        drink_selected.update()

        return jsonify({
            'success': True,
            'drinks': [drink_selected.long()]
        })

    except Exception as e:
        # Print exception error and rollback database session
        print(f'Exception "{e}" in edit_drink()')
        db.session.rollback()

# '''
# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json
#     {"success": True, "delete": id}
#     where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    """
    DELETE request to remove a drink from the database.
    --------------------
    Tested with:
        - Auth0 'DELETE /drinks/<id>'
    """
    # Query database the drink with the chosen ID
    drink_selected = Drink.query.filter(
        Drink.id == id).one_or_none()

    # If drink not found in database with id, raise 404
    if not drink_selected:
        abort(404)

    try:
        # Attempt to delete the drink from database
        drink_selected.delete()

        return jsonify({
            'success': True,
            'delete': id
        })

    except Exception as e:
        # Print exception error and rollback database
        print(f'Exception "{e}" in delete_drink()')
        db.session.rollback()

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    """422 Unprocessable App Error Handler"""
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# '''
# COMPLETED
# @TODO implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with appropriate messages):
#         jsonify({
#             "success": False,
#             "error": 404,
#             "message": "resource not found"
#             }), 404

# '''

# '''
# @TODO implement error handler for 404
#     error handler should conform to general task above
# '''

@app.errorhandler(404)
def not_found(error):
    """404 Not-Found App Error Handler"""
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    """400 Bad-Request App Error Handler"""
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """401 Unauthorized App Error Handler"""
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """403 Forbidden App Error Handler"""
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(500)
def internal_server_error(error):
    """500 Internal Server Error App Error Handler"""
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500

# '''
# @TODO implement error handler for AuthError
#     error handler should conform to general task above
# '''


@app.errorhandler(AuthError)
def auth_error(exception):
    """Auth-Error App Error Handler"""
    error_exception_json = jsonify(exception.error)
    error_code = exception.status_code

    return error_exception_json, error_code
