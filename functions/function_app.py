import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import logging
import os
from step_3_text_to_model.main import text_to_model_func, get_cosmos_items
from step_2_link_scraper.main import link_scraper
from step_1_jobindex_paginator.main import jobindex_paginator
from step_1_linkedin_paginator.main import linkedin_paginator

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Step 1 - Jobindex paginator (Timer trigger)
@app.function_name("JobindexPaginatorTimerTrigger")
@app.timer_trigger(schedule="0 0 * * *", arg_name="myTimer", run_on_startup=False)
def jobindex_paginator_timer_trigger(myTimer: func.TimerRequest) -> None:
    try:
        jobindex_paginator()
    except Exception as e:
        logging.warning(f"Jobindex paginator failed: {e}")

# Step 2 - Linkedin paginator (Timer trigger)
@app.function_name("LinkedinPaginatorTimerTrigger")
@app.timer_trigger(schedule="06 0 * * *", arg_name="myTimer", run_on_startup=False)
def linkedin_paginator_timer_trigger(myTimer: func.TimerRequest) -> None:
    try:
        linkedin_paginator()
    except Exception as e:
        logging.warning(f"Linkedin paginator failed: {e}")

# Step 3 - Link Scraper (Timer trigger)
@app.function_name("LinkScraperTimerTrigger")
@app.timer_trigger(schedule="12 0 * * *", arg_name="myTimer", run_on_startup=False)
def link_scraper_timer_trigger(myTimer: func.TimerRequest) -> None:
    try:
        link_scraper()
    except Exception as e:
        logging.warning(f"Link scraper failed: {e}")

# Step 4 - Text to Model (Timer trigger)
@app.function_name("TextToModelTimerTrigger")
@app.timer_trigger(schedule="18 0 * * *", arg_name="myTimer", run_on_startup=False)
def text_to_model_timer_trigger(myTimer: func.TimerRequest) -> None:
    try:
        items = get_cosmos_items()
        if items:
            logging.warning(f"{len(items)} entries found")
            text_to_model_func(items)
    except Exception as e:
        logging.warning(f"Text to model failed: {e}")
        
# Step 5 - Text to Model (HTTP trigger) - Callable Text to Model
@app.function_name("TextToModelHttpTrigger")
@app.route(route="textToModel", methods=["POST"])
def text_to_model_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        items = get_cosmos_items()
        if items:
            logging.warning(f"{len(items)} entries found")
            text_to_model_func(items)
            return func.HttpResponse(f"Processed {len(items)} items.", status_code=200)
        else:
            return func.HttpResponse("No items found.", status_code=200)
    except Exception as e:
        logging.warning(f"Text to model failed: {e}")
        return func.HttpResponse(f"Text to model failed: {e}", status_code=500)

