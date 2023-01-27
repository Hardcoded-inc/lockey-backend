import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: get_door(id, d), AuthLevels.USER)



def get_door(id, d):
    query_str ="SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE d.id = ? AND ud.user_id = ?"
    door = db.query_one(query_str, (id, auth_data["id"]))

    if (not door):
        return func.HttpResponse(json.dumps({"error": "Door not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(door, default=str), mimetype="application/json")
