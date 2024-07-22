from functools import wraps
from flask import request, jsonify
from util import decode_auth_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = auth_header.split(" ")[1]
            if token == "null":
                return jsonify({'message': 'Token is missing!'}), 403
            user_id = decode_auth_token(token)
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(user_id, *args, **kwargs)

    return decorated
