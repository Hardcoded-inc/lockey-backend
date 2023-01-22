import logging
from shared import db, jwt, cookie
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get all doors function processed a request.')

    conn = db.get_connection();
    cursor = conn.cursor();

    cursor.execute('SELECT * FROM doors')
    doors = cursor.fetchall()
    results = [tuple(row) for row in doors]

    return func.HttpResponse(json.dumps(results, default=str), mimetype="application/json")
