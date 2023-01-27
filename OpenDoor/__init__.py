import logging
from shared import db, web_pub_sub as wps
from shared.validate import validate
import azure.functions as func
import json
from shared.auth import auth, AuthLevels



def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: open_door(id, d), AuthLevels.USER)




def open_door(id: int, auth_data) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE dbo.doors SET is_open = \'True\''
        'WHERE id = ?',
        id
    )

    connection.commit()

    wps.publish_message_on_doors_update(auth_data)
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



