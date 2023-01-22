import logging
from shared import db, jwt, cookie
import azure.functions as func


def auth(req):
    token = cookie.read(req, "jwt")
    auth_data = jwt.decode(token)
    logging.warn(auth_data)

    return auth_data
