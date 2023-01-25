import logging
from shared import db, jwt, cookie
import azure.functions as func
import json
from typing import Optional
import bcrypt

JWT_TTL = 300 #sec

def main(req: func.HttpRequest) -> func.HttpResponse:
    domain = req.url.split("/")[2]
    return log_in_user(req.get_json(), domain)


def log_in_user(body: bytes, domain: str) -> func.HttpResponse:
    # 1. Get username
    username = body.get("username") or ""
    passwd = body.get("password") or ""
    logging.warn(passwd)


    # 2. Find user in DB (Return error if not found)
    user = db.query_one('SELECT id, username, is_admin, password_hash, password FROM dbo.users WHERE username=?', username)
    logging.warn(user)

    if user is None:
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")


    # 3. Check password
    encoded_passwd = passwd.encode('UTF-8')
    if not bcrypt.checkpw(encoded_passwd, user["password_hash"]):
        return func.HttpResponse(json.dumps({"error": "Invalid password"}), status_code=401, mimetype="application/json")


    # 4. Return Json Web Token
    data = { "id": user["id"], "username": user["username"], "is_admin": user["is_admin"] }
    token = jwt.create(data)


    # 5. Set jwt cookie
    jwt_cookie = cookie.gen(domain, JWT_TTL, "jwt", token)
    return func.HttpResponse(body=json.dumps({"jwt": token}), status_code=200, headers=jwt_cookie, mimetype="application/json")
