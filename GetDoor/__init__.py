import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: get_door(id, d), AuthLevels.USER)



def get_door(id, auth_data):
    doors = db.query_one("SELECT d.* from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE d.id = ?", id)

    if (not doors):
        return func.HttpResponse(json.dumps({"error": "Door not found"}), status_code=404, mimetype="application/json")

    users = db.query_all("SELECT ID, username, is_admin FROM users u LEFT JOIN users_doors ud ON u.id = ud.user_id WHERE ud.door_id = ?", id)
    doors['users'] = users

    return func.HttpResponse(json.dumps(doors, default=str), mimetype="application/json")
