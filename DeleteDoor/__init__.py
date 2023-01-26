import logging
from shared import db, context
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Delete Door (id: {id}) function processed a request.")

    return delete_door(id)

def delete_door(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    context.remove_middle_record_for(cursor, "door_id", id)
    cursor.execute('DELETE FROM doors WHERE id = ?', id)

    connection.commit()

    return func.HttpResponse(f"Door deleted successfully.")
