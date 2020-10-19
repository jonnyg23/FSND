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

db_drop_and_create_all()

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

    """
    try:
        selection = Drink.query.order_by(Drink.id).all()
        drinks = [drink.short() for drink in selection]

        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
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

    """
    try:
        selection = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in selection]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        print(f'Exception "{e}" in retrieve_drinks_detail()')

        return jsonify({
            'success': False
        })


# '''
# COMPLETED
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    """
    POST request to add a new drink to the database.
    --------------------
    Tested with:

    """
    body = request.get_json()

    if not body:  # Invalid json body
        abort(400)

    try:
        # Get parameters from body
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        # Create a new drink, using body as inputs
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        drink.insert()  # Insert into database

        return jsonify({
            'success': True,
            'drinks': drink.long()
        })

    except Exception as e:
        print(f'Exception "{e}" in create_drink()')
        db.session.rollback()

    finally:
        db.session.close()
        abort(500)


# '''
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(id):
    """
    PATCH request to edit drink in the database.
    --------------------
    Tested with:

    """
    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
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
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(500)
def internal_server_error(error):
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
    error_exception_json = jsonify(exception.error)
    error_code = exception.status_code

    return error_exception_json, error_code
