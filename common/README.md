# Common Package

This package contains common scripts used in various steps of scraping job posts and saving them to Cosmos DB.

## Installation

To install the `common` package, you need to have `pip` installed and a Personal Access Token (PAT) from GitHub.

Follow these steps:

1. Generate a Personal Access Token (PAT) on GitHub. Make sure to give it permission to private repos. For more information, see [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

2. Install the package using `pip`. Replace `your_pat` with your Personal Access Token.

```bash
pip install git+https://it-minds:your_pat@github.com/it-minds/itm_leads-finder-scripts.git@main#egg=common\&subdirectory=common
```

## Usage

```python
from common import CosmosDBClient

client = CosmosDBClient(
    COSMOS_DB_ENDPOINT,
    COSMOS_DB_PRIMARY_KEY,
    COSMOS_DB_DATABASE_NAME,
    COSMOS_DB_CONTAINER_NAME,
)
```
