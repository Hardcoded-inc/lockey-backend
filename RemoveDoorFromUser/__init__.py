import logging
from shared import db, web_pub_sub as wps
from shared.validate import validate
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



FIELDS = {"user_id", "door_id"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    return auth(req, lambda d: remove_door_from_user(req.get_json()), AuthLevels.ADMIN)


def remove_door_from_user(body):
    connection = db.get_connection()
    cursor = connection.cursor()

    if body:
        try:
            query = 'DELETE FROM dbo.users_doors WHERE user_id=? and door_id=?;'
            validated = validate(body, FIELDS)
            params = (validated["user_id"], validated["door_id"])

            cursor.execute(query, params)
            connection.commit()

            wps.notfiy_connected_clients('doors')

            return func.HttpResponse(f"User-Door record removed successfully.")

        except Exception as e:
            logging.error(e)
            pass

    return func.HttpResponse(
            "Bad data",
            status_code=400
    )
