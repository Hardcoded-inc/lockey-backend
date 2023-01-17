import logging
from shared import db
import json
import azure.functions as func

UPDATEABLE_COLUMNS = ['name']

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Update door function processed a request.')

    id = req.route_params.get('id')

    conn = db.get_connection()
    cursor = conn.cursor()

    body = req.get_json()
    door = body["door"]

    # Update a door in the SQL database
    cursor.execute(build_query(door, id), *list(door.values()))
    conn.commit()

    return func.HttpResponse(json.dumps({'message': "Door udpdated succesfully"}), mimetype="application/json")


def build_query(door: dict, id: int) -> str:
    updates = ''

    for col, value in door.items():
        if (col in UPDATEABLE_COLUMNS):
            updates = updates + "{} = ?, ".format(col)

    updates = updates[:-2]

    return 'UPDATE doors SET {} WHERE id = {}'.format(updates, id)
