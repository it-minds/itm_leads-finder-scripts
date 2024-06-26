# Link Scraper
This script takes the links from our Azure Cosmos DB, and utilizing the scraping library Beautiful Soup, we scrape all the text content from the page and store it on the same object in our DB with a different property name.

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

The script uses environment variables for configuration. You can set these variables in a `local.settings.json` file in the same directory as the script. (see `example.settings.json`)

