from boto3.dynamodb.conditions import Key
from models.product import Product
from typing import Optional
from .aws_session import AWSSession, handle_aws_error

# Constants
DYNAMODB_TABLE_NAME = 'StockTable'

# Initialize DynamoDB
dynamodb = AWSSession.get_resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

@handle_aws_error('DynamoDB query')
def query_item(part_id: str, store_id: str) -> Optional[Product]:
    print(f"Querying DynamoDB for part_id: {part_id} and store_id: {store_id}")
    response = table.query(
        KeyConditionExpression=Key('PartId').eq(part_id) & Key('StoreId').eq(store_id)
    )
    items = response['Items']
    if items is not None:
        print("Found item in DynamoDB")
        return product_from_dict(items[0])
    else:
        print("No items found in DynamoDB for part_id and store_id")
        return None

@handle_aws_error('DynamoDB put')
def put_item(product: Product) -> None:
    print(f"Putting item in DynamoDB: {product.id}")
    table.put_item(
        Item={
            'PartId': product.id,
            'StoreId': product.store.name,
            'Name': product.name,
            'Price': product.price,
            'Url': product.url,
            'InStock': product.in_stock
        }
    )
    print("Successfully put item in DynamoDB")

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
