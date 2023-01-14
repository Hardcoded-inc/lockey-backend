import logging
from shared import db
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('id')

    conn = db.get_connection()
    cursor = conn.cursor()

    body = req.get_json()
    user = body["user"]
    
    # Update a user in the SQL database
    cursor.execute(build_query(user, id), *list(user.values()))
    conn.commit()
    
    return func.HttpResponse(json.dumps({'message': "User udpdated succesfully"}), mimetype="application/json")


def build_query(user: dict, id: int) -> str:
    updates = ''

    for col, value in user.items():
        updates = updates + "{} = ?, ".format(col, value)
    
    updates = updates[:-2]

    return 'UPDATE users SET {} WHERE id = {}'.format(updates, id)
