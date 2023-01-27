import logging
from shared import db
import azure.functions as func
import json
from shared.auth import auth, AuthLevels


def main(req: func.HttpRequest) -> func.HttpResponse:
    return auth(req, lambda d: get_all_users(), AuthLevels.ADMIN)


def get_all_users():
    users = db.query_all('SELECT u.id, u.username, ud.door_id FROM users u LEFT JOIN users_doors ud ON u.id = ud.user_id')
    users_with_doors = list(filter(lambda u: u["door_id"], users))
    users_without_doors = list(filter(lambda u: not u["door_id"], users))

    for u in users_without_doors: u["doors"] = []
    users = users_without_doors

    for user in users_with_doors:
        door = db.query_one("SELECT * FROM doors WHERE id=?", user["door_id"])
        try:
            idx = list(u["id"] for u in users).index(user["id"])
            users[idx]["doors"].append(door)

        except Exception as e:
            users.append(user)
            users[-1]["doors"] = []
            users[-1]["doors"].append(door)

    users = list(removekey(u, "door_id") for u in users)
    logging.warn(users)

    return func.HttpResponse(json.dumps(users, default=str), mimetype="application/json")





def removekey(d, key):
    r = dict(d)
    del r[key]
    return r
