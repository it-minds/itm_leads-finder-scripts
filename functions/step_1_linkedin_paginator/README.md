# Linkedin Paginator

This script scrapes job listings from Linkedin and saves the links to Azure Cosmos DB.

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

The script uses environment variables for configuration. You can set these variables in a `local.settings.json` file in the same directory as the script. (See `example.settings.json`)
