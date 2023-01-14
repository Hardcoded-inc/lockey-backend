import logging
import azure.functions as func
import pyodbc
import os



def main(req: func.HttpRequest) -> func.HttpResponse:

    server = os.environ.get("SERVER")
    driver = os.environ.get("DRIVER")
    database = os.environ.get("DATABASE")
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')

    connection_string = 'DRIVER='+driver+';' \
                        'SERVER='+server+';' \
                        'DATABASE='+database+';' \
                        'UID='+username+';' \
                        'PWD='+ password

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Extract request parameters
    body = req.get_json()
    name = body['name']

    query = 'INSERT INTO dbo.doors (name) VALUES (?);'
    params = (name)

    cursor.execute(query, params)
    connection.commit()

    logging.warning(cursor.fetchall())


    doors_id = cursor.fetchone()[0]
    logging.warning("-------")
    logging.warning(doors_id)

    return func.HttpResponse(f'Doors with ID {doors_id} created successfully.')
