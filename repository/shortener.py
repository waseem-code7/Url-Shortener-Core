import common.utils
from repository.dynamoDBClient import DynamoDBClient
logger = common.utils.get_logger("ShortenerRepository")


class ShortenerRepository(DynamoDBClient):

    def __init__(self, table_name):
        super().__init__(table_name)

    def add_item_to_table(self, pk, sk, data: dict):
        try:
            attributes: dict = {
                "short_url_id": pk,
                "timestamp": sk
            }
            attributes.update(data)

            result = self.put_item(attributes)
            return result
        except Exception as e:
            logger.error(f"Error occurred while inserting data to dynamo db {e}")

