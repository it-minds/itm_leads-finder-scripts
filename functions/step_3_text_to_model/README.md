# Text to Json
This script handles converting the scraped text content into json attributes. This is done by parsing the raw text, a prompt describing what to do, and a class showing how the json should be structured, through a LLM (groq)

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

For the Groq api key see [GROQ API KEY](https://console.groq.com/keys)

For the Grog model we suggest just using the default of `llama3-70b-8192`
