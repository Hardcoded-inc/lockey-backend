import logging
from shared import db
import azure.functions as func
import json
from typing import Optional
import bcrypt


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python LogIn function processed a request.')

    return log_in_user(req.get_json())



def log_in_user(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    # 1. Get username
    username = body["username"]
    passwd = body["password"]
    logging.warn(passwd)


    # 2. Find user in DB (Return error if not found)

    # TODO: Change col name to password_hash
    cursor.execute('SELECT username, password FROM dbo.users WHERE username=?', username)
    user = cursor.fetchone()
    logging.warn(user)

    if user is None:
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")


    # 3. Get password
    # (user_username, user_pwd_hash) = user

    # TODO: Replace pwd hashing with extracting pwd hash dtraight from db
    (user_username, pwd) = user
    encoded_pwd = pwd.encode('UTF-8')
    user_pwd_hash = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
    logging.warn(user_pwd_hash)


    # 4. Check password
    encoded_passwd = passwd.encode('UTF-8')
    if not bcrypt.checkpw(encoded_passwd, user_pwd_hash):
        return func.HttpResponse(json.dumps({"error": "Invalid password"}), status_code=401, mimetype="application/json")


    # 6. Return Json Web Token
    jwt = "dupa"
    return func.HttpResponse(body=json.dumps({"jwt": jwt}), status_code=200, mimetype="application/json")




    # Save pwd like that:
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
