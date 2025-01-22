from product_resolvers.cc_resolver import CanadaComputersResolver
import os
from dotenv import load_dotenv
from aws_accessors import ssm_accessor, dynamodb_accessor
from discord import discord_publisher
from models.store import Store
from models.product import Product

# Load environment variables from .env file
load_dotenv()

PRODUCT_ID = "GSKILL RipJaws 32GB"
PRODUCT_URL = "https://www.canadacomputers.com/en/desktop-memory/99478/g-skill-ripjaws-v-32gb-2x16gb-ddr4-3200mhz-cl16-udimm-f4-3200c16d-32gvk.html"
PRODUCT_TITLE = "GSKILL RipJaws 32GB"

def find_product_availability() -> Product:
    resolver = CanadaComputersResolver(
        product_id=PRODUCT_ID,
        product_url=PRODUCT_URL,
        product_title=PRODUCT_TITLE
    )
    return resolver.resolve()

def publish_to_discord(product: Product) -> None:
    # Retrieve webhook from Parameter Store
    discord_webhook_url_arn = os.getenv('DISCORD_WEBHOOK_URL_ARN')
    discord_webhook_url = ssm_accessor.retrieve_parameter(discord_webhook_url_arn)
    discord_publisher.publish(discord_webhook_url, product)

def handle(event, context):
    product = find_product_availability()
    publish_to_discord(product)

    # Save the results to DynamoDB
    dynamodb_accessor.put_item(product)

    # Get product item from DynamoDB
    item = dynamodb_accessor.query_item(PRODUCT_ID, Store.CANADA_COMPUTERS.name)
    print(item)

    print("Published to Discord")

handle(None, None)
