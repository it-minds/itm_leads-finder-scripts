import azure.functions as func
import azure.durable_functions as df
import logging
from step_3_text_to_model.main import text_to_model_func, get_cosmos_items
from step_2_link_scraper.main import link_scraper
from step_1_jobindex_paginator.main import jobindex_paginator
from step_1_linkedin_paginator.main import linkedin_paginator

app = df.DFApp()

# A time-triggered function with a Durable Functions client binding
@app.durable_client_input(client_name="client")
@app.timer_trigger(schedule="0 0 * * *", arg_name="myTimer", run_on_startup=True)
async def leads_finder_timer_trigger(myTimer: func.TimerRequest, client: df.DurableOrchestrationClient):
    logging.warning("timer trigger started")
    await client.start_new("leads_finder_orchestrator")
    
    

# Orchestrator
@app.orchestration_trigger(context_name="context")
def leads_finder_orchestrator(context: df.DurableOrchestrationContext):
    logging.warning("orchestrator started")
    jobindex_result = yield context.call_activity("jobindex_paginator_activity")
    linkedin_result = yield context.call_activity("linkedin_paginator_activity")
    
    
    
    if not (jobindex_result and linkedin_result):
        logging.warning("jobindex/linkedin failed")
        return None
    
    link_scraper_result = yield context.call_activity("link_scraper_activity")
    
    if not link_scraper_result:
        logging.warning("link scraper failed")
        return None
    
    try:
        yield context.call_activity("text_to_model_activity")
    except Exception as e:
        logging.error(e)
    
        


# # Activities
# Jobindex paginator
@app.activity_trigger(input_name="input")
def jobindex_paginator_activity(input: str):
    logging.warning("jobindex paginator started")
    try:
        jobindex_paginator()
    except Exception as e:
        logging.warning(f"Jobindex paginator failed: {e}")
        return False
    return True

# Linkedin paginator
@app.activity_trigger(input_name="input")
def linkedin_paginator_activity(input: str):
    try:
        linkedin_paginator()
    except Exception as e:
        logging.warning(f"Linkedin paginator failed: {e}")
        return False
    return True

# Link scraper
@app.activity_trigger(input_name="input")
def link_scraper_activity(input: str):
    try:
        link_scraper()
    except Exception as e:
        logging.warning(f"Link scraper failed: {e}")
        return False
    return True

# Text to model
@app.activity_trigger(input_name="input")
def text_to_model_activity(input: str):
    try:
        items = get_cosmos_items()
        if len(items) > 0:
            logging.warning(f"{len(items)} entries found")
            text_to_model_func(items)         
    except Exception as e:
        logging.warning(e)
