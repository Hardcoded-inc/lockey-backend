import logging
import json
import os
from shared import db
from azure.messaging.webpubsubservice import WebPubSubServiceClient

def publish_message_on_doors_update(auth_data):
    connection_string = os.environ.get("WPSCONNSTR")
    hub = os.environ.get("WPSHUB")

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub)

    if(auth_data["is_admin"]):
        doors = db.query_all('SELECT * FROM doors')
    else:
        doors = db.query_all("SELECT * from doors d LEFT JOIN users_doors ud ON d.id = ud.door_id  WHERE ud.user_id = ?", auth_data["id"])



    service.send_to_all(json.dumps(doors, default=str))
