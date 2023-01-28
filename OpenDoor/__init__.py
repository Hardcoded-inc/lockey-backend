import logging
from shared import db, web_pub_sub as wps
from shared.validate import validate
import azure.functions as func
import json
from shared.auth import auth, AuthLevels
import requests
import threading
import os

API_URL = os.environ.get('API_URL')


def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: open_door(id, d, req.headers), AuthLevels.USER)




def open_door(id: int, auth_data, headers) -> func.HttpResponse:
    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE dbo.doors SET is_open = \'True\''
        'WHERE id = ?',
        id
    )

    connection.commit()

    start_delayed_close_door(id, headers)
    wps.publish_message_on_doors_update(auth_data)

    return func.HttpResponse("true", status_code=200)

def start_delayed_close_door(id, headers):
    fire_and_forget(API_URL + '/doors/{}/close'.format(id), json.dumps({'delay': 10}), headers)

def request_task(url, json, headers):
    print(url)
    requests.post(url, json, headers=headers)

def fire_and_forget(url, json, headers):
    threading.Thread(target=request_task, args=(url, json, headers)).start()



