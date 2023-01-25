import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    door = db.query_one('SELECT * FROM dbo.doors WHERE id = ?', id)


    if (not door):
        return func.HttpResponse(json.dumps({"error": "Door not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(door, default=str), mimetype="application/json")
