import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    id = req.route_params.get('id')

    conn = db.get_connection()
    cursor = conn.cursor()


    cursor.execute(
            'SELECT * FROM users WHERE id = ?',
            id
        )
    user = cursor.fetchone()

    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(tuple(user), default=str), mimetype="application/json")