# Jobindex Paginator

This script scrapes job listings from a jobindex and saves the links to Azure Cosmos DB.

## Getting Started

Follow these steps to get the project started:

1. Create a Python virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

For MacOS
```bash
source venv/bin/activate
```
For Windows
```bash
.\venv\Scripts\activate
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

The script uses environment variables for configuration. You can set these variables in a `.env` file in the same directory as the script. Here's an example:

```env
BASE_URL=https://www.jobindex.dk/jobsoegning/it/systemudvikling/danmark?page=
MAX_PAGES=100
START_PAGE=1
RETRY_DELAY_SECONDS=10
MAX_ATTEMPTS=3
COSMOS_DB_ENDPOINT=https://leads-finder-db.documents.azure.com:443/
COSMOS_DB_PRIMARY_KEY=your-primary-key
COSMOS_DB_DATABASE_NAME=your-database-name
COSMOS_DB_CONTAINER_NAME=your-container-name
```
