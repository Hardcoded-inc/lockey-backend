import logging
from shared import db
import azure.functions as func
import json
from typing import Optional
from shared.auth import auth, AuthLevels


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Delete User (id: {id}) function processed a request.")
    auth_data = auth(req, AuthLevels.ADMIN)

    return delete_user(id)



def delete_user(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', id)
    connection.commit()


    return func.HttpResponse(f"User deleted successfully.")
