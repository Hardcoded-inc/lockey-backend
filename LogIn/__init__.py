import logging
from shared import db
import azure.functions as func
import json
from typing import Optional

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python LogIn function processed a request.')

    return log_in_user(req.get_json())



def log_in_user(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    # 1. Get username
    username = body["username"]

    # 2. Find user in DB (Return error if not found)

    cursor.execute('SELECT username, password FROM dbo.users WHERE username=?', username)
    user = cursor.fetchone()
    logging.warn(user)

    if user is None:
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")


    # 3. Get password
    (user_username, user_password) = user

    # 4. Hash password


    # 5. Compare hashes

    # 6. Return Json Web Token


    jwt = "dupa"

    return func.HttpResponse(body=json.dumps({"jwt": jwt}), status_code=200, mimetype="application/json")
