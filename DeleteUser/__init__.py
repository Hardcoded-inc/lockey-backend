import logging
from shared import db, context
import azure.functions as func
import json
from typing import Optional
from shared.auth import auth, AuthLevels


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')

    return auth(req, lambda d: delete_user(id), AuthLevels.ADMIN)


def delete_user(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    context.remove_middle_record_for(cursor, "user_id", id)
    cursor.execute('DELETE FROM users WHERE id = ?', id)
    # connection.commit()


    return func.HttpResponse(f"User deleted successfully.")
