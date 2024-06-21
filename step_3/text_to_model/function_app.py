import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import datetime
import json
import logging
import os
from main import text_to_model_func, get_cosmos_items

app = func.FunctionApp()

connection_str = os.environ.get("AzureWebJobsServiceBus")
queue_trigger_name = os.environ.get("AzureWebJobsServiceBusQueueTriggerName")
queue_output_name = os.environ.get("AzureWebJobsServiceBusQueueOutputName")



@app.function_name("TextToModelServiceBusQueueTrigger")
@app.service_bus_queue_trigger(arg_name="msg", connection="AzureWebJobsServiceBus", queue_name=queue_trigger_name)
def text_to_model_servicebus_queue_trigger(msg: func.ServiceBusMessage):
    try:
        items = get_cosmos_items()
        if items:
            logging.info(f"{len(items)} entries found - proccessing 10")
            text_to_model_func(items[:10])
            # Send a message to the Service Bus
            with ServiceBusClient.from_connection_string(connection_str) as client:
                sender = client.get_queue_sender(queue_name=queue_output_name)
                with sender:
                    message = ServiceBusMessage("Text to model completed")
                    sender.send_messages(message)
                    
    except Exception as e:
        logging.warning(f"text_to_model failed: str {e}") 
    