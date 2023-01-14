import logging
from shared import db
from shared.validate import validate
import azure.functions as func
import json


FIELDS = {"name"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Create Door function processed a request.")

    return create_door(req.get_json())


def create_door(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    if body:
        try:
            query = 'INSERT INTO dbo.doors (name) VALUES (?);'
            validated = validate(body["door"], FIELDS)
            params = (validated["name"])

            cursor.execute(query, params)
            connection.commit()

            return func.HttpResponse(f"Door created successfully.")

        except Exception as e:
            logging.error(e)
            pass

    return func.HttpResponse(
            "Bad data",
            status_code=400
    )



