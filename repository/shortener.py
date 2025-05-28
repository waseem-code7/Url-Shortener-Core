import os

import common.utils
from repository.dynamoDBClient import DynamoDBClient
logger = common.utils.get_logger("ShortenerRepository")


class ShortenerRepository(DynamoDBClient):

    def __init__(self, table_name):
        super().__init__(table_name)

    def put_item_to_table(self, pk, data: dict, return_values="ALL_OLD"):
        try:
            attributes: dict = {
                os.getenv("DYNAMO_URL_TABLE_PK", default="short_url_id"): pk
            }
            attributes.update(data)

            result = self.put_item(attributes, return_values)
            return result
        except Exception as e:
            logger.error(f"Error occurred while inserting data to dynamo db {e}")

    def update_param_in_record(self, pk, param_key, param_value, return_values="UPDATED_NEW"):
        try:
            key_attributes = {
                os.getenv("DYNAMO_URL_TABLE_PK", default="short_url_id"): pk
            }
            result = self.update_param(key_attributes, param_key, param_value, return_values)
            return result
        except Exception as e:
            logger.error(f"Error occurred while updating data to dynamo db {e}")

    def delete_record_from_table(self, pk, return_values="NONE"):
        try:
            key_attributes = {
                os.getenv("DYNAMO_URL_TABLE_PK", default="short_url_id"): pk
            }
            return self.delete_record(key_attributes, return_values)
        except Exception as e:
            logger.error(f"Error occurred while deleting data from dynamo db {e}")


    def get_item_from_table(self, pk):
        try:
            key_attributes = {
                os.getenv("DYNAMO_URL_TABLE_PK", default="short_url_id"): pk
            }
            return self.get_item(key_attributes)
        except Exception as e:
            logger.error(f"Error occurred while attempting to get data from dynamo db {e}")

