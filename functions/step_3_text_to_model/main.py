from datetime import datetime
from common import TextToModel, CosmosDBClient
import os, logging
from dotenv import load_dotenv
from .json_model import JobPostingModel, TechnologyGroupEnum
from .quality_control import check_quality, clean_job_posting_groups

load_dotenv()


def get_client() -> CosmosDBClient:
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
    return client

def get_cosmos_items():
    # Inits client
    client = get_client()
    # Selects all entries that are only on "step 2" and no errors are present, or they are on step 2 with the RateLimitError from Groq
    query = """
        SELECT * FROM c 
        WHERE (NOT IS_DEFINED(c.error) AND c.step = 2) 
        OR 
        (c.step = 2 AND CONTAINS(c.error.failure_reason, 'RateLimitError'))
        OR
        (c.step = 2 AND CONTAINS(c.error.failure_reason, 'OutputParserException'))
        OR
        (c.step = 2 AND CONTAINS(c.error.failure_reason, 'TypeError'))
    """

    # Fetching all items from db which have completed step 2
    items = client.fetch_items_by_query(query)
    return items

def text_to_model_func(items):
    
    # Inits client
    client = get_client()
    
    text_to_model = TextToModel(JobPostingModel)


    error_count = 0
    success_count = 0

    starttime = datetime.now()
    for (i,item) in enumerate(items):
        response = text_to_model.generate_model(item["text"])
        
        #Error handling for prompt_llama3_to_json
        if isinstance(response, str):
            logging.warning(f"Error in parsing text to json, entry id = {item['id']} - {str(response)}")
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
        else:
            try:
                del item["error"]
            except KeyError as e:
                logging.warning("No error to be deleted")
            
        clean_job_posting_groups(response)
        

        
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
            "groups": response.groups
        }
        
        # Merge llm_populated_data with item
        llm_populated_data = {**item, **llm_populated_data}
        
        resp = client.update_item(llm_populated_data["id"], llm_populated_data)
        logging.warning(f"Created item with id: {llm_populated_data['id']}")
        if resp == None:
            logging.warning(f"failed to update item : {llm_populated_data['id']}")
            
        if "error" in llm_populated_data:
            error_count += 1
        else:
            success_count += 1
            
        if len(items) >= 10 and i % (len(items) // 10) == 0:
            logging.warning(f"Completed {(i / len(items) * 100)+ 10:.0f}% - with {error_count} errors, and {success_count} successes")
            logging.warning(datetime.now() - starttime)   
            
    logging.warning(f"Updated {success_count} items sucessfully in the DB - {error_count} failed - out of a total of {len(items)}")