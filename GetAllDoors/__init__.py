import logging
from shared import db
from shared.auth import auth
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get all doors function processed a request.')
    session = auth(req)

    get_all_doors(session)

def get_all_doors():
    conn = db.get_connection();
    cursor = conn.cursor();

    id = None if session["is_admin"] else session["id"]
    if id:
        # TODO: Add querying doors for specific user
        cursor.execute('SELECT * FROM doors')
    else:
        cursor.execute('SELECT * FROM doors')

    doors = cursor.fetchall()
    results = [tuple(row) for row in doors]

    return func.HttpResponse(json.dumps(results, default=str), mimetype="application/json")
