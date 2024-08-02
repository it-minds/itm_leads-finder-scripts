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
    

# A HttpTriggered function that starts the orchestrator
@app.route(route="custom")
@app.durable_client_input(client_name="client")
async def leads_finder_http_trigger(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    logging.warning("Http trigger triggered")
    instance_id = await client.start_new("leads_finder_orchestrator")
    return instance_id
    

# Orchestrator
@app.orchestration_trigger(context_name="context")
def leads_finder_orchestrator(context: df.DurableOrchestrationContext):
    logging.warning("orchestrator started")
    try:
        jobindex_result = yield context.call_activity("jobindex_paginator_activity")
        linkedin_result = yield context.call_activity("linkedin_paginator_activity")
    
    
    
        if not (jobindex_result and linkedin_result):
            logging.warning("jobindex/linkedin failed")
            return None
        
        link_scraper_result = yield context.call_activity("link_scraper_activity")
        
        if not link_scraper_result:
            logging.warning("link scraper failed")
            return None
        
        items = get_cosmos_items()
        logging.warning(f"Items fetched - {len(items)}")
        continuation_token = {'start_index': 0, 'items': items}

        while continuation_token:
            logging.warning(continuation_token['start_index'])
            result = yield context.call_activity('text_to_model_activity', continuation_token)
            continuation_token = result.get('continuation_token')
            if result.get('status') == "completed":
                break

        return "All activities completed successfully"
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
def text_to_model_activity(input: dict):
    items = input.get('items', [])
    start_index = input.get('start_index', 0)
    batch_size = 8  # Adjust based on what can be processed within 5 minutes

    try:
        if start_index < len(items):
            batch = items[start_index:start_index + batch_size]
            text_to_model_func(batch)
            
            # Return continuation token if there are more items
            if start_index + batch_size < len(items):
                logging.warning("continuation token return")
                return {
                    'continuation_token': {
                        'start_index': start_index + batch_size,
                        'items': items
                    }
                }
        logging.warning("status returned")
        return {'status': 'completed'}
    except Exception as e:
        logging.error(f"Error in text_to_model_activity: {e}")
        raise
