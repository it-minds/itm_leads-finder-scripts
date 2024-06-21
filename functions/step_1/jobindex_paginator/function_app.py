import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import datetime
import json
import logging
import os
from main import jobindex_paginator

app = func.FunctionApp()

connection_str = os.environ.get("AzureWebJobsServiceBus")
queue_output_name = os.environ.get("AzureWebJobsServiceBusQueueOutputName")



@app.function_name("JobindexPaginatorTimerTrigger")
@app.schedule(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def jobindex_paginator_timer_trigger(timer: str):
    try:
        jobindex_paginator()
    except Exception as e:
        logging.warning(f"jobindex paginator failed: str {e}") 
    # Send a message to the Service Bus
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(queue_name=queue_output_name)
        with sender:
            message = ServiceBusMessage("jobindex Paginator completed")
            sender.send_messages(message)