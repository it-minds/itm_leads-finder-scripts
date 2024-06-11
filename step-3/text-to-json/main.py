from datetime import datetime
from common import prompt_llama3_to_json, CosmosDBClient
from dotenv import load_dotenv
import os
from json_model import JobPostingModel
from quality_control import json_model_quality_control

load_dotenv()

# Azure Cosmos DB vars
COSMOS_DB_ENDPOINT = os.environ["COSMOS_DB_ENDPOINT"]
COSMOS_DB_PRIMARY_KEY = os.environ["COSMOS_DB_PRIMARY_KEY"]
COSMOS_DB_DATABASE_NAME = os.environ["COSMOS_DB_DATABASE_NAME"]
COSMOS_DB_CONTAINER_NAME = os.environ["COSMOS_DB_CONTAINER_NAME"]

# Initialize Azure Cosmos DB client
client = CosmosDBClient(
    COSMOS_DB_ENDPOINT,
    COSMOS_DB_PRIMARY_KEY,
    COSMOS_DB_DATABASE_NAME,
    COSMOS_DB_CONTAINER_NAME,
)


# This is the general prompt we use for extracting specific infomation about the job
prompt = """Your task is to analyze the job posting from the user message. Extract the necessary fields 
in accordance with the provided output schema and constraints. If any of these fields cannot be determined, their values should be set to null."""

# Fetching all items from db which have completed step 2
items = client.fetch_items_step_3()


for item in items:
    response = prompt_llama3_to_json(prompt, item["text"], JobPostingModel)
    
    #Error handling for prompt_llama3_to_json
    if isinstance(response, str):
        print(f"Error in parsing text to json, entry id = {item['id']} - {str(response)}")
        continue
    
    item["step"] = 3
    item["step_3_timestamp"] = datetime.now().isoformat()
    
    #Different quality controls
    failure_reason = json_model_quality_control(response, item['id'])
    if isinstance(failure_reason, str):
        error_obj = {
            "step" : 3,
            "timestamp" : datetime.now().isoformat(),
            "failure_reason" : failure_reason
        }
        item["error"] = error_obj

    

    
    #create new object for data from the llm
    llm_populated_data = {
        "position": response.position,
        "company": response.company,
        "job_description": response.job_description,
        "contact_name": response.contact_name,
        "contact_phone": response.contact_phone,
        "contact_email": response.contact_email,
        "technologies": response.technologies,
        "experience": response.experience,
        "required_qualifications": response.required_qualifications,
        "location": response.location,
        "job_type": response.job_type,
        "industry": response.industry,
        "application_deadline": response.application_deadline,
        "posting_time": response.posting_time,
    }
    
    # Merge llm_populated_data with item
    llm_populated_data = {**item, **llm_populated_data}
    
    try:
        client.update_item(llm_populated_data["id"], llm_populated_data)
    except Exception as e:
        print(f"failed to update item : {llm_populated_data['id']} - error : {e}")
        
print(f"Updated {len(items)} items in the DB")