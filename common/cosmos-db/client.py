from azure.cosmos import CosmosClient, exceptions, PartitionKey
import logging


class CosmosDBClient:
    def __init__(self, endpoint, primary_key, database_name, container_name):
        self.client = CosmosClient(endpoint, primary_key)
        self.database_name = database_name
        self.container_name = container_name

        # Create or get the database
        self.database = self.client.create_database_if_not_exists(id=self.database_name)

        # Create or get the container
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400,
        )

    def upload_items(self, item):
        try:
            self.container.create_item(body=item)
        except exceptions.CosmosHttpResponseError as e:
            logging.info(
                f"An error occurred while creating item with id {item['id']}: {str(e)}"
            )
