import logging
from shared import db, context
import azure.functions as func
import json
from typing import Optional


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Delete User (id: {id}) function processed a request.")

    return delete_user(id)

def delete_user(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    context.remove_middle_record_for(cursor, "user_id", id)
    cursor.execute('DELETE FROM users WHERE id = ?', id)
    connection.commit()


    return func.HttpResponse(f"User deleted successfully.")
