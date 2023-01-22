import logging
import os
import jwt

def create(data):
    jwt_secret = os.environ.get("JWT_SECRET")
    encoded = jwt.encode(data, jwt_secret, algorithm="HS256")
    return encoded

def decode(data):
    jwt_secret = os.environ.get("JWT_SECRET")

    try:
        decoded = jwt.decode(data, jwt_secret, algorithms=["HS256"])
        return decoded

    except Exception as e:
        logging.error(e)
        return None

