import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'NamePerCity'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        name = body['name']
        city = body['city']
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid request format",
                "error": str(e)
            })
        }

    table = dynamodb.Table(TABLE_NAME)

    try:
        table.put_item(
            Item={
                'City': city,
                'PersonName': name
            }
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to insert item into DynamoDB",
                "error": str(e)
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Item inserted successfully",
            "data": {
                "name": name,
                "city": city
            }
        })
    }