import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get Door function processed a request.')

    id = req.route_params.get('id')

    conn = db.get_connection()
    cursor = conn.cursor()


    cursor.execute(
            'SELECT * FROM dbo.doors WHERE id = ?',
            id
        )

    door = cursor.fetchone()

    if (not door):
        return func.HttpResponse(json.dumps({"error": "Door not found"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(tuple(door), default=str), mimetype="application/json")
