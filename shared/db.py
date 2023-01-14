import pyodbc
import os

def get_connection():
    # Set up connection to SQL database

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

    return pyodbc.connect(connection_string)
