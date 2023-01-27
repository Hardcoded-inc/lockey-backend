import logging
from shared import db
from shared.validate import validate
import azure.functions as func
import json
from shared.auth import auth, AuthLevels


FIELDS = {"name", "long", "lat"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    return auth(req, lambda d: create_door(req.get_json()), AuthLevels.ADMIN)


def create_door(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    if body:
        try:
            query = 'INSERT INTO dbo.doors (name, long, lat) VALUES (?, ?, ?);'
            validated = validate(body["door"], FIELDS)
            params = (validated["name"], validated["long"], validated["lat"])

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



