from dotenv import dotenv_values
import pyodbc

def get_connection():
    # Set up connection to SQL database
    env_values = dotenv_values()

    server = env_values["SERVER"]
    driver = env_values["DRIVER"]
    database = env_values["DATABASE"]
    username = env_values['DB_USERNAME']
    password = env_values['DB_PASSWORD']

    connection_string = 'DRIVER='+driver+';' \
                        'SERVER='+server+';' \
                        'DATABASE='+database+';' \
                        'UID='+username+';' \
                        'PWD='+ password

    return pyodbc.connect(connection_string)
    