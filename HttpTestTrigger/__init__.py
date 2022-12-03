# import logging

# import azure.functions as func


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )


# import os
# import pyodbc
# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from urllib.parse import quote_plus 
# import azure.functions as func

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     server = 'lockey-server.database.windows.net'
#     database = 'LockeyDB'
#     username = 'CloudSA7eec8125'
#     password = ''
#     port = os.getenv('PORT',default=1433)
#     driver = '{ODBC Driver 13 for SQL Server}'
#     #connect using parsed URL
#     odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password
#     connect_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(odbc_str)
#     # #connect with sa url format
#     # sa_url = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}"
#     engine = create_engine(connect_str)
#     return func.HttpResponse(
#             'Success',
#             status_code=200
#     )




import logging
import azure.functions as func
import os
import pyodbc
import struct

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_string = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+database
    #When MSI is enabled
    if os.getenv("MSI_SECRET"):
        conn = pyodbc.connect(connection_string+';Authentication=ActiveDirectoryMsi')

    #Used when run from local
    else:
        SQL_COPT_SS_ACCESS_TOKEN = 1256

        # exptoken = b''
        # for i in bytes(db_token, "UTF-8"):
        #     exptoken += bytes({i})
        #     exptoken += bytes(1)

        # tokenstruct = struct.pack("=i", len(exptoken)) + exptoken
        # conn = pyodbc.connect(connection_string, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct })
        # Uncomment below line when use username and password for authentication
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    while row:
        print(row[0])
        row = cursor.fetchone()

    return func.HttpResponse(
            'Success',
            status_code=200
    )