from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from common import CosmosDBClient
import hashlib, os, time, requests
from azure.cosmos import exceptions

load_dotenv()

# Crawling vars
BASE_URL = os.environ["BASE_URL"]
MAX_PAGES = int(os.environ["MAX_PAGES"])  # Set the maximum number of pages to scrape
START_PAGE = int(os.environ["START_PAGE"])  # Set the starting page on jobindex
RETRY_DELAY_SECONDS = int(
    os.environ["RETRY_DELAY_SECONDS"]
)  # Set the delay before retrying a page
MAX_ATTEMPTS = int(
    os.environ["MAX_ATTEMPTS"]
)  # Set the maximum number of attempts to scrape the page

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

# Dynamic vars
page_number = START_PAGE
last_page = MAX_PAGES + START_PAGE
attempts = 0
all_links = []  # List to store all links
error_count = 0

while page_number < last_page:
    print(f"Processing page {page_number}...")
    url = BASE_URL + str(page_number)
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = [a["href"] for a in soup.find_all("a", class_="seejobdesktop", href=True)]

    # Retry the current page if no links are found
    if not links:
        attempts += 1
        print(f"No links found, retrying after delay... Attempt count: {attempts}")
        if attempts >= MAX_ATTEMPTS:
            print("Maximum retries reached, stopping.")
            break
        time.sleep(RETRY_DELAY_SECONDS)
        continue

    # Reset the retry count if links are found
    attempts = 0

    # Add links to the list
    all_links.extend(links)

    page_number += 1  # Increment the page number


# Save links to Azure Cosmos DB
for link in all_links:
    hashed_link = hashlib.sha1(link.encode("utf-8")).hexdigest()
    item = {
        "id": hashed_link,
        "step_1_timestamp": datetime.now().isoformat(),
        "step": 1,
        "link": link,
        "source": "jobindex",
    }
    cosmos_response: exceptions.CosmosHttpResponseError | None = client.upload_items(item)
    if isinstance(cosmos_response, exceptions.CosmosHttpResponseError):
        error_count += 1

print(f"Saved {len(all_links) - error_count} links to Azure Cosmos DB, with {error_count} errors happening out of a total of {len(all_links)} - See cosmosDB Insights for more info")
