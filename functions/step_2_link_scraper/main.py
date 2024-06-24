import os
from datetime import datetime
from common import CosmosDBClient
from tenacity import retry, stop_after_attempt, wait_fixed
import requests
from bs4 import BeautifulSoup
from .quality_control import html_text_quality_control

#Using the requests package to extract entire HTML page from a link, wrapped in retry logic if a 400 status happens
@retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
def get_html_document(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad response status codes
    return response.text


def get_html_text_content(link):
    
    try:
        html_document = get_html_document(link["link"])
    except Exception as e:
        print(f"failed to get html doc - {e} - for entry with id: {link['id']}")
        return None
    try:
        # Create soup object
        soup = BeautifulSoup(html_document, 'html.parser') 
    except Exception as e:
        print("failed to get soup object",e)
        return None
    
    return soup.get_text("-", True).replace("\n", "")



def link_scraper():

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
    error_count = 0
    success_count = 0
    
    # Selects all entries that are only on "step 1"
    query = "SELECT * FROM c WHERE c.step = 1" 

    # Fetches all entries in db which are ready for step 2 (Marked as step = 1 in DB)
    links = client.fetch_items_by_query(query)


    # Loops through each link and retrieves the text content of the html pages, finally updates the entry in DB with text content and updated step
    for link in links:

        html_text_content = get_html_text_content(link)
        
        failure_reason = html_text_quality_control(html_text_content)
        
        if failure_reason:
            error_obj = {
                "step" : 2,
                "timestamp" : datetime.now().isoformat(),
                "failure_reason" : failure_reason
            }
            link["error"] = error_obj

        
        # Update link object with new information
        link["text"] = "" if html_text_content is None else html_text_content
        link["step"] = 2
        link["step_2_timestamp"] = datetime.now().isoformat()

        resp = client.update_item(link["id"], link)
        if resp == None: 
            print(f"failed to update item - id: {link['id']}")
            
        if "error" in link:
            error_count += 1
        else:
            success_count += 1

    print(f"Updated {success_count} items sucessfully in the DB - {error_count} failed - out of a total of {len(links)}")





