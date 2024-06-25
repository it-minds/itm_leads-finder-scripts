# Azure Functions Application

This repository contains an Azure Functions application that processes data through a series of steps involving pagination, scraping, and data transformation.

## Project Structure

- **function_app.py**: Contains the main logic for the Azure Functions, including triggers and function definitions.
- **local.settings.json**: Stores local settings and configurations, including environment variables - see `example.settings.json` for actual values used in this project.
- **host.json**: Contains global configuration options that affect all functions in the function app.
- **requirements.txt**: Lists the Python packages required for the project.

## function_app.py Overview

The `function_app.py` file defines several Azure Functions, each responsible for a specific part of the data processing pipeline:

1. **Jobindex Paginator (Timer Trigger)**:
    - Triggered daily at midnight.
    - Paginates through Jobindex listings and sends a message to the Service Bus.

2. **Linkedin Paginator (Service Bus Queue Trigger)**:
    - Triggered by a message from the Service Bus.
    - Paginates through LinkedIn listings and sends a message to the next Service Bus queue.

3. **Link Scraper (Service Bus Queue Trigger)**:
    - Triggered by a message from the Service Bus.
    - Scrapes links and sends a message to the next Service Bus queue.

4. **Text to Model (Service Bus Queue Trigger)**:
    - Triggered by a message from the Service Bus.
    - Processes items from Cosmos DB and transforms text data to a model format.

## Environment Variables

Copy the content of `example.settings.json` into a new file called `local.settings.json` and fill out the correct values. This is the equivelant of a `.env`.

## Running the Application

1. Install the required packages:

    ```bash
    python -m venv venv
    ```
2. Activate the virtual environment

    ```bash
    .\venv\Scripts\Activate
    ```
3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
4. Start the Azure Functions runtime:

    ```bash
    func start
    ```
