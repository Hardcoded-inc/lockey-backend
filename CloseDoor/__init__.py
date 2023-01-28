import logging
from shared import db, web_pub_sub as wps
from shared.validate import validate
import azure.functions as func
import json
from shared.auth import auth, AuthLevels
import time



def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    body = json.loads(req.get_body())

    if ('delay' in body):
        time.sleep(body['delay'])
        
    return auth(req, lambda d: close_door(id, d), AuthLevels.USER)



def close_door(id: int, auth_data) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    
    cursor.execute(
        'UPDATE dbo.doors SET is_open = \'False\''
        'WHERE id = ?',
        id
    )

    connection.commit()

    wps.publish_message_on_doors_update(auth_data)
    return func.HttpResponse("true")


