import logging
from shared import db
import azure.functions as func
import json
from typing import Optional
from shared.auth import auth


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    logging.info(f"Delete User (id: {id}) function processed a request.")
    auth_data = auth(req)

    if(auth_data and auth_data["is_admin"]):
        return delete_user(id)
    else:
        return func.HttpResponse(f"Unauthorized", status_code=403)



def delete_user(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', id)
    connection.commit()


    return func.HttpResponse(f"User deleted successfully.")
