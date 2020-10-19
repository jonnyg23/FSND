from flask import Flask, request, abort
from functools import wraps


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        abort(401)

    elif header_parts[0].lower() != 'bearer':
        abort(401)

    return header_parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        abort(403)

    return True

def requires_auth(permission='')
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


app = Flask(__name__)


# @app.route('/headers')
# @requires_auth
# def headers(jwt):
#     # @TODO unpack the request header
#     print(jwt)
#     return 'not implemented'

@app.route('/image')
@requires_auth('get:images')
def images(jwt):
    # @TODO unpack the request header
    print(jwt)
    return 'not implemented'
