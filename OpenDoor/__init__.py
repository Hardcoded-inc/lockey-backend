import logging
from shared import db
from shared.validate import validate
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Door (id: {id} ) function processed a request.")

    return open_door(id)



def create_door(body: bytes) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute(
        'SELECT is_open FROM doors WHERE id = ?',
        id
    )
    door = cursor.fetchone()

    if not door["is_open"]:
        cursor.execute('UPDATE doors SET is_open = true WHERE id = ?', id)

        # Set timer and lock door again after 10 sek



#     user = cursor.fetchone()
#
#     if (not user):
#         return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")
#
#     return func.HttpResponse(json.dumps(tuple(user), default=str), mimetype="application/json")
#
#
#
#
#     return func.HttpResponse(
#             "Bad data",
#             status_code=400
#     )
#


