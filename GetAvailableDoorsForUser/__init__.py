import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels




def main(req: func.HttpRequest) -> func.HttpResponse:
    id = req.route_params.get('id')
    return auth(req, lambda d: get_available_doors_for_user(id), AuthLevels.ADMIN)


def get_available_doors_for_user(id):
    user = db.query_one('SELECT * FROM dbo.users WHERE id = ?', id)

    if (not user):
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    user['available_doors'] = db.query_all(build_query(), id)

    return func.HttpResponse(json.dumps(user, default=str), mimetype="application/json")

def build_query():
    return '''SELECT * FROM doors AS d
                LEFT OUTER JOIN users_doors AS ud ON d.id = ud.door_id
                WHERE ud.user_id IS NULL OR ud.user_id != ?'''
