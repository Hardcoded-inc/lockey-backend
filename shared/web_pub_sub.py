import logging
import json
import os
from shared import db
from azure.messaging.webpubsubservice import WebPubSubServiceClient

def notfiy_connected_clients(resource_name):
    connection_string = os.environ.get("WPSCONNSTR")
    hub = os.environ.get("WPSHUB")

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub)

    service.send_to_all(json.dumps({'modified_resource': resource_name}, default=str))
