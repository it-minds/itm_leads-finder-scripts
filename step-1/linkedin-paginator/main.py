import hashlib
from azure.cosmos import exceptions
import time
from urllib.parse import urlparse, urlunparse
from common import CosmosDBClient
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

load_dotenv()

# # Url vars
# Used for accessing the "next page"
START = 0





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

attempts = 0
all_links = []  # List to store all links

error_count = 0
#Helper function
def clean_url(url):
    # Parse the URL into its components
    parsed_url = urlparse(url)

    # Construct a new URL without query parameters
    clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

    return clean_url

while START < 999:
    
    # The url consists of the query params for finding jobs in denmark, marked as "software developer" and sorted by most recent posts.
    url =f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software+developer&location=denmark&f_TPR=r86400&start={START}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = []
    
    # Find link and date posten and append to object
    for li in soup.find_all("li"):
        a_tag = li.find("a", class_="base-card__full-link", href=True)
        time_tag = li.find("time", class_="job-search-card__listdate--new", datetime=True)

        if a_tag and time_tag:
            links.append({
                "link": clean_url(a_tag["href"]),
                "timeago": time_tag["datetime"]
            })

    
    # Retry the current page if no links are found
    if not links:
        attempts += 1
        print(f"No links found, retrying after delay... Attempt count: {attempts}, at start={START}")
        if attempts >= 2:
            print("Maximum retries reached, stopping.")
            break
        time.sleep(2)
        continue
    
    # Reset the retry count if links are found
    attempts = 0
    
    # Add links to the list
    all_links.extend(links)
    
    # Increment start for showing more posts
    print(f"At start {START}")
    START += 10
    

# Save links to Azure Cosmos DB
for link in all_links:
    hashed_link = hashlib.sha1(link["link"].encode("utf-8")).hexdigest()
    item = {
        "id": hashed_link,
        "step_1_timestamp": datetime.now().isoformat(),
        "step": 1,
        "link": link["link"],
        "time_posted": time_tag["datetime"],
        "source": "linkedin",
    }
    cosmos_response = client.upload_items(item)
    if isinstance(cosmos_response, exceptions.CosmosHttpResponseError):
        error_count += 1
    

print(f"Saved {len(all_links) - error_count} links to Azure Cosmos DB, with {error_count} errors happening out of a total of {len(all_links)} - See cosmosDB Insights for more info")

