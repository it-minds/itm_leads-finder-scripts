import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import logging
import os
from step_3_text_to_model.main import text_to_model_func, get_cosmos_items
from step_2_link_scraper.main import link_scraper
from step_1_jobindex_paginator.main import jobindex_paginator
from step_1_linkedin_paginator.main import linkedin_paginator

app = func.FunctionApp()

connection_str = os.environ.get("AzureWebJobsServiceBus")
step_1_trigger_name = os.environ.get("ServiceBusStep1Trigger")
step_2_trigger_name = os.environ.get("ServiceBusStep2Trigger")
step_3_trigger_name = os.environ.get("ServiceBusStep3Trigger")


# # # # # Step 1
# # Jobindex paginator (Timer trigger)
@app.function_name("JobindexPaginatorTimerTrigger")
@app.timer_trigger(schedule="0 0 * * *", arg_name="myTimer", run_on_startup=False)
def jobindex_paginator_timer_trigger(myTimer: func.TimerRequest) -> None:
    try:
        jobindex_paginator()
    except Exception as e:
        logging.warning(f"jobindex paginator failed: str {e}") 
    # Send a message to the Service Bus
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(queue_name=step_1_trigger_name)
        with sender:
            message = ServiceBusMessage("jobindex Paginator completed")
            sender.send_messages(message)

# # Linkedin paginator (Servicebus queue trigger)
@app.function_name("LinkedinPaginatorServiceBusQueueTrigger")
@app.service_bus_queue_trigger(arg_name="msg", connection="AzureWebJobsServiceBus", queue_name=step_1_trigger_name)
def linkedin_paginator_servicebus_queue_trigger(msg: func.ServiceBusMessage):
    try:
        linkedin_paginator()
    except Exception as e:
        logging.warning(f"linkedind paginator failed: str {e}") 
    # Send a message to the Service Bus
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(queue_name=step_2_trigger_name)
        with sender:
            message = ServiceBusMessage("Linkedin Paginator completed")
            sender.send_messages(message)

# # # # # Step 2
# # Link Scraper (Servicebus queue trigger)
@app.function_name("LinkScraperServiceBusQueueTrigger")
@app.service_bus_queue_trigger(arg_name="msg", connection="AzureWebJobsServiceBus", queue_name=step_2_trigger_name)
def link_scraper_servicebus_queue_trigger(msg: func.ServiceBusMessage):
    try:
        link_scraper()
    except Exception as e:
        logging.warning(f"linkedind paginator failed: str {e}") 
    # Send a message to the Service Bus
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(queue_name=step_3_trigger_name)
        with sender:
            message = ServiceBusMessage("Link Scraper completed")
            sender.send_messages(message)

# # # # # Step 3
# # Text to Model (Servicebus queue trigger)
@app.function_name("TextToModelServiceBusQueueTrigger")
@app.service_bus_queue_trigger(arg_name="msg", connection="AzureWebJobsServiceBus", queue_name=step_3_trigger_name)
def text_to_model_servicebus_queue_trigger(msg: func.ServiceBusMessage):
    try:
        items = get_cosmos_items()
        if items:
            logging.warning(f"{len(items)} entries found - proccessing 10")
            text_to_model_func(items)
            # Send a message to the Service Bus
            # with ServiceBusClient.from_connection_string(connection_str) as client:
            #     sender = client.get_queue_sender(queue_name=step_3_trigger_name)
            #     with sender:
            #         message = ServiceBusMessage("Text to model completed")
            #         sender.send_messages(message)
                    
    except Exception as e:
        logging.warning(f"text_to_model failed: str {e}") 