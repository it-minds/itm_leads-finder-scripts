# Text to Json
This script handles converting the scraped text content into json attributes. This is done by parsing the raw text, a prompt describing what to do, and a class showing how the json should be structured, through a LLM (groq)

## Getting Started

Follow these steps to get the project started:

1. Create a Python virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

The script uses environment variables for configuration. You can set these variables in a `.env` file in the same directory as the script. 

For the Groq api key see [GROQ API KEY](https://console.groq.com/keys)

For the Grog model we suggest just using the default of `llama3-70b-8192`

Here's an example:
```env
GROQ_MODEL=select-groq-llm-model
GROQ_API_KEY=your-groq-api-key
COSMOS_DB_ENDPOINT=your-cosmos-db-endpoint
COSMOS_DB_PRIMARY_KEY=your-primary-key
COSMOS_DB_DATABASE_NAME=your-database-name
COSMOS_DB_CONTAINER_NAME=your-container-name
```
