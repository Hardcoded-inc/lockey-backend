import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



def main(req: func.HttpRequest) -> func.HttpResponse:
    return auth(req, lambda d: get_doors(d), AuthLevels.USER)


def get_doors(auth_data):
    doors = []

    if(auth_data["is_admin"]):
        doors = db.query_all('SELECT * FROM doors')
    else:
        doors = db.query_all("SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE ud.user_id = ?", auth_data["id"])


    return func.HttpResponse(json.dumps(doors, default=str), mimetype="application/json")
