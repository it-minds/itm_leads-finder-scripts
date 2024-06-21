import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import datetime
import json
import logging
import os
from main import link_scraper

app = func.FunctionApp()

connection_str = os.environ.get("AzureWebJobsServiceBus")
queue_trigger_name = os.environ.get("AzureWebJobsServiceBusQueueTriggerName")
queue_output_name = os.environ.get("AzureWebJobsServiceBusQueueOutputName")



@app.function_name("LinkScraperServiceBusQueueTrigger")
@app.service_bus_queue_trigger(arg_name="msg", connection="AzureWebJobsServiceBus", queue_name=queue_trigger_name)
def link_scraper_servicebus_queue_trigger(msg: func.ServiceBusMessage):
    try:
        link_scraper()
    except Exception as e:
        logging.warning(f"linkedind paginator failed: str {e}") 
    # Send a message to the Service Bus
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(queue_name=queue_output_name)
        with sender:
            message = ServiceBusMessage("Link Scraper completed")
            sender.send_messages(message)