import logging
from shared import db
import azure.functions as func
import json
from typing import Optional
import bcrypt
from shared.auth import auth, AuthLevels


USER_FIELDS = {"username", "password", "is_admin"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    return auth(req, lambda d: create_user(req.get_body()), AuthLevels.ADMIN)

def create_user(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()
    user = parse_user_data(body)

    if user:
        password_hash = generate_password_hash(user["password"])
        params = (user["username"], user["password"], password_hash, user["is_admin"])

        # Insert a new user into the SQL database
        cursor.execute(
            "INSERT INTO dbo.users (username, password, password_hash, is_admin) "
            "VALUES (?, ?, ?, ?)",
            params
        )
        connection.commit()
        return func.HttpResponse(f"User created successfully.")
    
    return func.HttpResponse(f"Bad user data", status_code=400)

def parse_user_data(body: bytes) -> Optional[dict]:
    try:
        body_dict = json.loads(body)
    except:
        return None

    return validate_user_data(body_dict)

def validate_user_data(body_dict: dict) -> Optional[dict]:
    if ("user" in body_dict):
        user = body_dict["user"]

        if (USER_FIELDS <= user.keys()):
            return user;

def generate_password_hash(password):
    encoded_password = password.encode('UTF-8')
    password_hash = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return password_hash


