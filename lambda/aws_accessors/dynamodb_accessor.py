import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from models.product import Product
from typing import Optional
import os

# Get profile from environment variable or use default
aws_profile = os.getenv('AWS_PROFILE', 'default')
print(f"Using AWS profile: {aws_profile}")

DYNAMODB_TABLE_NAME = 'StockTable'
table = boto3.resource('dynamodb', region_name='us-east-1', profile_name=aws_profile).Table(DYNAMODB_TABLE_NAME)

def query_item(part_id: str, store_id: str) -> Optional[Product]:
    print(f"Querying DynamoDB for part_id: {part_id} and store_id: {store_id}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PartId').eq(part_id) & Key('StoreId').eq(store_id)
        )
        items = response['Items']
        if "Items" in response and response['Items'] is not None:
            print(f"Found {len(response['Items'])} items in DynamoDB")
            return product_from_dict(response['Items'][0])
        else:
            print("No items found in DynamoDB for part_id and store_id")
            return None
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        raise e
    except Exception as e:
        print(f"Unexpected Exception: {str(e)}")
        raise e

def put_item(item: Product) -> None:
    print(f"Putting item into DynamoDB: {item}")
    try:
        table.put_item(Item=product_to_dict(item))
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        raise e
    except Exception as e:
        print(f"Unexpected Exception: {str(e)}")
        raise e

def product_to_dict(product: Product) -> dict:
    return {
        'PartId': product.id,
        'StoreId': product.store.name,
        'Name': product.name,
        'Price': product.price,
        'Url': product.url,
        'InStock': product.in_stock
    }

def product_from_dict(unstructured_item: dict) -> Product:
    return Product(
        id=unstructured_item['PartId'],
        store=unstructured_item['StoreId'],
        name=unstructured_item['Name'],
        price=unstructured_item['Price'],
        url=unstructured_item['Url'],
        in_stock=unstructured_item['InStock']
    )
