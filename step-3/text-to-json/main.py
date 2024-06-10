from common import prompt_to_llama3_json, CosmosDBClient
from dotenv import load_dotenv
import os

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

