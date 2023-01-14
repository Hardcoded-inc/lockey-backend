import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    conn = db.get_connection();
    cursor = conn.cursor();

    cursor.execute(
            'SELECT * FROM users',
        )
    users = cursor.fetchall()
    results = [tuple(row) for row in users]
    
    return func.HttpResponse(json.dumps(results, default=str), mimetype="application/json")