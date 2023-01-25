import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('id')
    user = db.query_one('SELECT * FROM dbo.users WHERE id = ?', id)
    doors = db.query_all("SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE ud.user_id = ?", user["ID"])
    user["doors"] = doors

    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(user, default=str), mimetype="application/json")

