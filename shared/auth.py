import logging
from shared import db, jwt, cookie
import azure.functions as func

def auth(req):
    token = req.headers.get("Bareer")
    auth_data = jwt.decode(token)
    logging.warn(auth_data)
    # {'id': 1, 'username': 'FirstUser', 'is_admin': False}

    return auth_data
