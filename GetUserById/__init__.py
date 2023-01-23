import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('id')
    user = db.query_one('SELECT * FROM dbo.users WHERE id = ?', id)


    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(user, default=str), mimetype="application/json")
