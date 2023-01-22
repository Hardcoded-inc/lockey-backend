import logging
from shared import db, jwt, cookie
import azure.functions as func
import json
from typing import Optional
import bcrypt

JWT_TTL = 300 #sec

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python LogIn function processed a request.')
    domain = req.url.split("/")[2]

    return log_in_user(req.get_json(), domain)


def log_in_user(body: bytes, domain: str) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    # 1. Get username
    username = body["username"]
    passwd = body["password"]
    logging.warn(passwd)


    # 2. Find user in DB (Return error if not found)

    cursor.execute('SELECT username, is_admin, password_hash, password FROM dbo.users WHERE username=?', username)
    user = cursor.fetchone()
    logging.warn(user)

    if user is None:
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")


    # 3. Get password
    (user_username, user_is_admin, user_pwd_hash, user_password) = user


    # 4. Check password
    encoded_passwd = passwd.encode('UTF-8')
    if not bcrypt.checkpw(encoded_passwd, user_pwd_hash):
        return func.HttpResponse(json.dumps({"error": "Invalid password"}), status_code=401, mimetype="application/json")


    # 5. Return Json Web Token
    data = { "username": user_username, "user_is_admin": user_is_admin }
    token = jwt.create(data)


    # 6. Set jwt cookie
    jwt_cookie = cookie.gen(domain, JWT_TTL, "jwt", token)
    return func.HttpResponse(body=json.dumps({"jwt": token}), status_code=200, headers=jwt_cookie, mimetype="application/json")


