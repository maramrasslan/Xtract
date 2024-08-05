import jwt
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
SECRET_KEY = env_vars.get("SESSION_KEY")

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['userId']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
