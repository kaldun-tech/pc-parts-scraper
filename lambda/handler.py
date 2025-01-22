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
    """
    Finds the availability of a product by its ID, URL, and title.
    """
    resolver = CanadaComputersResolver(
        product_id=PRODUCT_ID,
        product_url=PRODUCT_URL,
        product_title=PRODUCT_TITLE
    )
    return resolver.resolve()

def publish_to_discord(product: Product) -> None:
    """
    Publishes a product to Discord.
    """
    # Retrieve webhook from Parameter Store
    discord_webhook_url_arn = os.getenv('DISCORD_WEBHOOK_URL_ARN')
    discord_webhook_url = ssm_accessor.retrieve_parameter(discord_webhook_url_arn)
    discord_publisher.publish(discord_webhook_url, product)

def handle(event, context):
    """
    Entry point for the Lambda function.
    """
    product = find_product_availability()
    previous = dynamodb_accessor.query_item(PRODUCT_ID, Store.CANADA_COMPUTERS.name)

    if previous is None:
        print("First run for this product- save to DynamoDB")
        dynamodb_accessor.put_item(product)
        # Only publish if product is in stock
        if product.in_stock:
            publish_to_discord(product)
            print("Case 2: Product is initially in stock. Published to Discord")
        else:
            print("Case 1: Product is initially out of stock. Do not publish to Discord")

    # Product is out of stock
    elif previous is not None and not product.in_stock:
        if previous.in_stock:
            print("Case 4: Product was previously in stock. Save to DB, do not publish.")
            dynamodb_accessor.put_item(product)
        else:
            print("Case 5: Product was already out of stock. Do not save to DB or publish")

    # Product is in stock
    elif previous is not None and product.in_stock:
        if previous.in_stock:
            print("Case 3: Product was already in stock. Do not save to DB or publish")
        else:
            print("Case 6: Product was previously out of stock. Save to DB and publish to Discord")
            dynamodb_accessor.put_item(product)
            publish_to_discord(product)

handle(None, None)
