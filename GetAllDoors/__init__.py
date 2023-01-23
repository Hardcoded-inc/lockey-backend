import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get all doors function processed a request.')

    doors = db.query_all('SELECT * FROM doors')
    return func.HttpResponse(json.dumps(doors, default=str), mimetype="application/json")
