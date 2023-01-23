import logging

import azure.functions as func


FIELDS = {"user_id", "door_id"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python AssignDoorToUser function processed a request.')

    return assign_door_to_user(req.get_json())


def assign_door_to_user(body):
    connection = db.get_connection()
    cursor = connection.cursor()

    #TODO
    if body:
        try:
            query = 'INSERT INTO dbo.users_doors (user_id, door_id) VALUES (?, ?);'
            validated_params = validate(body["door"], FIELDS)

            cursor.execute(query, validated_params)
            connection.commit()

            return func.HttpResponse(f"User-Door record created successfully.")

        except Exception as e:
            logging.error(e)
            pass

    return func.HttpResponse(
            "Bad data",
            status_code=400
    )

