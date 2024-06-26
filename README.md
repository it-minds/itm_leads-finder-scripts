# ITM Leads Finder Scripts
This repository contains scripts for scraping job posts from various sources, processing the data, and saving it to Azure Cosmos DB. The project is structured into multiple steps, each handled by different scripts.

## Overview
 - [Internal](#internal)
    - [Common](#common)
        - [CosmosDB Client](#cosmosdb-client)
        - [Text To Model Client](#text-to-model-client)
 - [Functions](#functions) 
   - [Step 1](#step-1)
      - [Jobindex Paginator](#jobindex-paginator)
      - [Linkedin Paginator](#linkedin-paginator)
   - [Step 2](#step-2)
      - [Link Scraper](#link-scraper)
   - [Step 3](#step-3)
      - [Text to Model](#text-to-model)

## Internal
### Common
#### CosmosDB Client
The CosmosDBClient class provides methods for interacting with Azure Cosmos DB, including creating or retrieving databases and containers, uploading items, fetching items based on specific steps, and updating existing items. It handles errors using logging and returns the appropriate responses.
#### Text to Model Client
The TextToModel class uses a Pydantic model and a GROQ model to convert raw text into structured output. The class initializes a ChatGroq instance and provides a method to generate structured models from input text, handling errors and validating the output against the Pydantic model.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/internal/README.md)

## Functions
The project runs via an Azure Function App, but can also be run locally.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/functions/README.md)
### Step 1
#### Jobindex Paginator
The Jobindex Paginator script scrapes job listings from Jobindex and saves the extracted links to Azure Cosmos DB.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/functions/step_1_jobindex_paginator/README.md)
#### Linkedin Paginator
The Linkedin Paginator script scrapes job listings from Jobindex and saves the extracted links to Azure Cosmos DB.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/functions/step_1_linkedin_paginator/README.md)


### Step 2
#### Link Scraper
The Link Scraper script retrieves links from Azure Cosmos DB and uses the Beautiful Soup library to scrape all text content from the linked pages. It then updates the database objects with the scraped content.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/functions/step_2_link_scraper/README.md)

### Step 3
#### Text to Model
The Text to JSON script converts scraped text content into structured JSON attributes using a Large Language Model (LLM) from Groq. It parses the raw text based on a given prompt and a class defining the JSON structure.

[*See specific README for more details*](https://github.com/it-minds/itm_leads-finder-scripts/blob/main/functions/step_3_text_to_model/README.md)