from datetime import datetime
from common import TextToModel, CosmosDBClient
from dotenv import load_dotenv
import os
from json_model import JobPostingModel
from quality_control import json_model_quality_control
import importlib

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

text_to_model = TextToModel(JobPostingModel)


# This is the general prompt we use for extracting specific infomation about the job
prompt = """Your task is to analyze the job posting from the user message. Extract the necessary fields 
in accordance with the provided output schema and constraints. If any of these fields cannot be determined, their values should be set to null."""

# Fetching all items from db which have completed step 2
items = client.fetch_items_step_3()
error_count = 0
success_count = 0

for item in items:
    response = text_to_model.generate_model(item["text"])
    
    #Error handling for prompt_llama3_to_json
    if isinstance(response, str):
        print(f"Error in parsing text to json, entry id = {item['id']} - {str(response)}")
        error_obj = {
            "step" : 3,
            "timestamp" : datetime.now().isoformat(),
            "failure_reason" : response
        }
        item["error"] = error_obj
        client.update_item(item["id"], item)
        error_count +=1
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
    
    
    resp = client.update_item(llm_populated_data["id"], llm_populated_data)
    if resp == None:
        print(f"failed to update item : {llm_populated_data['id']}")
        
    if "error" in llm_populated_data:
        error_count += 1
    else:
        success_count += 1

        
print(f"Updated {success_count} items sucessfully in the DB - {error_count} failed - out of a total of {len(items)}")