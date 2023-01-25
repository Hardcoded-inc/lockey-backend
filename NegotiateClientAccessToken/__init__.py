import logging
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import azure.functions as func
import json



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connection_string = "Endpoint=https://lockeypubsub.webpubsub.azure.com;AccessKey=aiFQe2o7bxk6H3ArSg4SqiCRzaOxKmzvvYjoY6CLwcM=;Version=1.0;"
    hub = "LockeyHub"

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub)

    token = service.get_client_access_token()
    
    return func.HttpResponse(json.dumps({'url': token['url']}, default=str), mimetype="application/json")

    
