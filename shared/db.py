import pyodbc
import os
import logging

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


def query_all(query_str, params=None):
    cursor = query(query_str, params)
    return [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]

def query_one(query_str, params=None):
    cursor = query(query_str, params)
    return dict(zip([column[0] for column in cursor.description], cursor.fetchone()))


def query(query_str, params):
    conn = get_connection();
    cursor = conn.cursor();

    if(params):
        cursor.execute(query_str, params)
    else:
        cursor.execute(query_str)

    return cursor
