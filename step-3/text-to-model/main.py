from datetime import datetime
from common import TextToModel, CosmosDBClient
from dotenv import load_dotenv
import os
from json_model import JobPostingModel
from quality_control import check_quality

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

# Fetching all items from db which have completed step 2
items__ = client.fetch_items_step_3()
items = items__[:10]
error_count = 0
success_count = 0

starttime = datetime.now()
for (i,item) in enumerate(items):
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
    failure_reason = check_quality(response)
    if failure_reason["marked"]:
        error_obj = {
            "step" : 3,
            "timestamp" : datetime.now().isoformat(),
            "failure_reason" : failure_reason["reasons"]
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
        "education": response.education,
        "location": response.location,
        "fulltime": response.fulltime,
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
        
    if len(items) >= 10 and i % (len(items) // 10) == 0:
        print(f"Completed {(i / len(items) * 100)+ 10:.0f}% - with {error_count} errors, and {success_count} successes")
        print(datetime.now() - starttime)   
        
print(f"Updated {success_count} items sucessfully in the DB - {error_count} failed - out of a total of {len(items)}")