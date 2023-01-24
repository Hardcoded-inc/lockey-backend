import logging
from shared import db
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Get available doors for user function processed a request.')
    id = req.route_params.get('id')

    user = db.query_one('SELECT * FROM dbo.users WHERE id = ?', id)

    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    user['available_doors'] = db.query_all(build_query(), id)

    return func.HttpResponse(json.dumps(user, default=str), mimetype="application/json")

def build_query():
    return '''SELECT * FROM doors AS d
                LEFT OUTER JOIN users_doors AS ud ON d.id = ud.door_id
                WHERE ud.user_id IS NULL OR ud.user_id != ?'''