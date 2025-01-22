import boto3
from botocore.exceptions import ClientError
from models.product import Product
import os

# Get profile from environment variable or use default
aws_profile = os.getenv('AWS_PROFILE', 'default')
print(f"Using AWS profile: {aws_profile}")

DYNAMODB_TABLE_NAME = 'StockTable'
table = boto3.resource('dynamodb', region_name='us-east-1', profile_name=aws_profile).Table(DYNAMODB_TABLE_NAME)

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
