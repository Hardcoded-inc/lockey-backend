import logging
from shared import db, jwt, cookie
import azure.functions as func
from enum import Enum


class AuthLevels():
    GUEST = 0
    USER = 1
    ADMIN = 2


def auth(req, action, auth_threshold = AuthLevels.GUEST):
    token = req.headers.get("Bareer")
    auth_data = jwt.decode(token)
    # logging.warn(auth_data)
    # E.g: {'id': 1, 'username': 'FirstUser', 'is_admin': False}

    if(auth_threshold <= get_current_auth_level(auth_data)):
        return action(auth_data)

    return func.HttpResponse(f"Unauthorized", status_code=403)




def get_current_auth_level(data):
    if(not data): return AuthLevels.GUEST
    if(data["is_admin"]): return AuthLevels.ADMIN
    return AuthLevels.USER
