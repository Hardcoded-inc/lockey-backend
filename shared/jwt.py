import os
import jwt

def create(data):
    jwt_secret = os.environ.get("JWT_SECRET")
    encoded = jwt.encode(data, jwt_secret, algorithm="HS256")
    return encoded

def decode(jwt):
    jwt_secret = os.environ.get("JWT_SECRET")
    jwt.decode(jwt, jwt_secret, algorithms=["HS256"])
    return decoded
