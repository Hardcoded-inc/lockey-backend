import logging
from shared import db, context
import azure.functions as func
import json
from shared.auth import auth, AuthLevels

def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')

    return auth(req, lambda d: delete_door(id), AuthLevels.ADMIN)

def delete_door(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    context.remove_middle_record_for(cursor, "door_id", id)
    cursor.execute('DELETE FROM doors WHERE id = ?', id)

    connection.commit()

    return func.HttpResponse(f"Door deleted successfully.")
