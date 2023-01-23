import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    users = db.query_all('SELECT u.id, u.username, u.is_admin FROM users u')
#
#
#     cursor.execute(
#             'SELECT d.id, d.name, d.is_open FROM doors'
#             'LEFT JOIN users_doors ud ON u.id = ud.user_id '
#             'LEFT JOIN doors d ON d.id = ud.door_id '
#
#         )
#     users = cursor.fetchall()

    return func.HttpResponse(json.dumps(users, default=str), mimetype="application/json")
