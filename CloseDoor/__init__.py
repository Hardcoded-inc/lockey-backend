import logging
from shared import db
from shared.validate import validate
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Door (id: {id} ) function processed a request.")

    return close_door(id)



def close_door(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE dbo.doors SET is_open = \'False\''
        'WHERE id = ?',
        id
    )

    connection.commit()

    return func.HttpResponse("true")


