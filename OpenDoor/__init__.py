import logging
from shared import db
from shared.validate import validate
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return open_door(id)



def open_door(id: int) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    door = db.query_one('SELECT * FROM dbo.doors WHERE id = ?', id)

    if door == None:
        return func.HttpResponse("Not found", status_code=404)

    cursor.execute(
        'UPDATE dbo.doors SET is_open = \'True\''
        'WHERE id = ?',
        id
    )

    connection.commit()
    return func.HttpResponse("true", status_code=200)


#     elif not door["is_open"]:
#         cursor.execute('UPDATE dbo.doors SET is_open = \'True\' WHERE id = ?', id)
#         connection.commit()
#         # TODO: Set timer and lock door again after 10 sek or sth (good idea)
#         return func.HttpResponse(True, status_code=200)
#
#     else:
#         return func.HttpResponse(f"Door is already open.", status_code=200)
#



