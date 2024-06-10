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
            
    def fetch_items_step_2(self):
        query = "SELECT * FROM c WHERE c.step = 1" # Selects all entries that are only on "step 1"
        items = []
        
        try:
            for item in self.container.query_items(query=query, enable_cross_partition_query=True):
                items.append(item)
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occured: {e.message}")
        return items 
    
    
    def update_item(self, item_id, updated_data):
        try:
            # Read the item to update
            item = self.container.read_item(item=item_id, partition_key=item_id)
            
            # Update the item with new data
            for key, value in updated_data.items():
                item[key] = value

            # Replace the item in the container
            response = self.container.replace_item(item=item, body=item)
            return response
        except exceptions.CosmosHttpResponseError as e:
            logging.info(f"An error occurred while updating item with id {item_id}: {str(e)} ")
            return None
        
