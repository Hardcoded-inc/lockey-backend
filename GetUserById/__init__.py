import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: get_user_by_id(id), AuthLevels.ADMIN)


def get_user_by_id(id):
    user = db.query_one('SELECT * FROM dbo.users WHERE id = ?', id)
    doors = db.query_all("SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE ud.user_id = ?", user["ID"])
    user["doors"] = doors

    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(user, default=str), mimetype="application/json")

