import boto3
from mypy_boto3_dynamodb.service_resource import Table

dynamodb = boto3.resource('dynamodb')


class DynamoDBClient:

    def __init__(self, table_name):
        self.table_name = table_name
        self.client: Table = dynamodb.Table(table_name)

    def put_item(self, attributes: dict, return_values):
        if attributes is None:
            raise Exception("Attributes cannot be None")

        return self.client.put_item(
            Item = attributes,
            ReturnValues = return_values
        )

    def get_item(self, key_attributes: dict):
        if key_attributes is None:
            raise Exception("Partition key cannot be None")
        return self.client.get_item(
            Key = key_attributes
        )

    def update_param(self, key_attributes: dict, param_key: str, param_value, return_value):
        if key_attributes is None:
            raise Exception("Partition key cannot be None")
        if param_key is None:
            raise Exception("Param key cannot be None")
        if param_value is None:
            raise Exception("Param value cannot be None")

        def get_expression_condition(attributes):
            conditionExpression = ""
            for key, value in attributes.items():
                conditionExpression += f"attribute_exists({key}) AND"
            return conditionExpression

        def clean_expression_condition(expression: str):
            return expression.rstrip().removesuffix(" AND")

        expression = get_expression_condition(key_attributes)
        cleaned_expression = clean_expression_condition(expression)

        return self.client.update_item(
            Key=key_attributes,
            UpdateExpression=f"SET {param_key} = :val",
            ExpressionAttributeValues={
                ":val": param_value
            },
            ReturnValues=return_value,
            ConditionExpression=cleaned_expression
        )

    def delete_record(self, key_attributes, return_values):
        if key_attributes is None:
            raise Exception("Partition key cannot be None")

        return self.client.delete_item(
            Key=key_attributes,
            ReturnValues=return_values
        )
