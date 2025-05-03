import boto3
dynamodb = boto3.resource('dynamodb')

class DynamoDBClient:

    def __init__(self, table_name):
        self.table_name = table_name
        self.client = dynamodb.Table(table_name)

    def put_item(self, attributes: dict = None):
        if attributes is None:
            raise Exception("Attributes cannot be None")

        return self.client.put_item(
            Item = attributes
        )