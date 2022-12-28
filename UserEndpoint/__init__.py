import azure.functions as func
import pyodbc
from dotenv import dotenv_values


def main(req: func.HttpRequest) -> func.HttpResponse:

    print("-------")
    print(req.params)

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

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Extract request parameters
    action = req.params.get('action')
    user_id = req.params.get('user_id')
    username = req.params.get('username')
    is_admin = req.params.get('is_admin')
    password = req.params.get('password')

    # Select the appropriate action
    if action == 'create':
        # Insert a new user into the SQL database
        cursor.execute(
            'INSERT INTO dbo.users (username, password, is_admin) '
            'VALUES (?, ?, ?)',
            username, password, is_admin
        )
        connection.commit()
        return func.HttpResponse(f'User with ID {user_id} created successfully.')
    elif action == 'read':
        # Select a user from the SQL database
        cursor.execute(
            'SELECT * FROM users WHERE id = ?',
            user_id
        )
        user = cursor.fetchone()
        return func.HttpResponse(f'User with ID {user_id}: {user}')
    elif action == 'read_all':
        # Select a user from the SQL database
        cursor.execute(
            'SELECT * FROM users',
        )
        users = cursor.fetchall()
        return func.HttpResponse(f'Users {users}')
    elif action == 'update':
        # Update a user in the SQL database
        cursor.execute(
            'UPDATE users SET username = ?, is_admin = ?, password = ? '
            'WHERE id = ?',
            username, is_admin, password, user_id
        )
        connection.commit()
        return func.HttpResponse(f'User with ID {user_id} updated successfully.')
    elif action == 'delete':
        # Delete a user from the SQL database
        cursor.execute(
            'DELETE FROM users WHERE id = ?',
            user_id
        )
        connection.commit()
        return func.HttpResponse(f'User with ID {user_id} deleted successfully.')

    # Return an error if the action is invalid
    return func.HttpResponse(f'Invalid action: {action}', status_code=400)
