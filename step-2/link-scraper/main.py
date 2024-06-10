from dotenv import load_dotenv
import os
from datetime import datetime
from common import CosmosDBClient
from tenacity import retry, stop_after_attempt, wait_fixed
import requests
from bs4 import BeautifulSoup


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

#Using the requests package to extract entire HTML page from a link, wrapped in retry logic if a 400 status happens
@retry(stop=stop_after_attempt(5), wait=wait_fixed(5), reraise=True)
def get_html_document(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad response status codes
    return response.text

links = client.fetch_all_step_2()

for link in links:
    try:
        html_document = get_html_document(link["link"])
    except Exception as e:
        print(f"failed to get html doc - {e}")
    # Create soup object
    try:
        soup = BeautifulSoup(html_document, 'html.parser') 
    except Exception as e:
        print("failed to get soup object",e)
        
    html_text_content = soup.get_text("-", True).replace("\n", "")
    link["text"] = html_text_content
    link["step"] = 2
    
    link["step_2_timestamp"] = datetime.now().isoformat()



