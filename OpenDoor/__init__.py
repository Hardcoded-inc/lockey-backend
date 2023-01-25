import logging
from shared import db
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

    query_str ="SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE d.id = ? AND ud.user_id = ?"
    door = db.query_one(query_str, (id, auth_data["id"]))

    if door == None:
        return func.HttpResponse("Unauthorized", status_code=403)

    if(door):
        cursor.execute(
            'UPDATE dbo.doors SET is_open = \'True\''
            'WHERE id = ?',
            door["id"]
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



