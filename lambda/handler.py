import os

from dotenv import load_dotenv

from aws_accessors import dynamodb_accessor, ssm_accessor
from discord.discord_publisher import publish as discord_publish
from models.product import Product
from models.store import Store
from product_resolvers.amazon_resolver import AmazonResolver
from product_resolvers.newegg_resolver import NeweggResolver

# Load environment variables from .env file
load_dotenv()

# Product configuration
PRODUCT_ID = "NVIDIA-RTX-3090TI-FE"
PRODUCT_TITLE = "NVIDIA GeForce RTX 3090 TI Founders Edition"
AMAZON_URL = "https://www.amazon.com/Nvidia-RTX-3090-TI-Founders/dp/B09X4JVZB5"
NEWEGG_URL = "https://www.newegg.com/p/1FT-0004-007S1"

def find_product_availability() -> list[Product]:
    """
    Finds the availability of a product across multiple retailers.
    Returns a list of Product objects, one for each retailer.
    """
    products = []
    
    # Check Amazon
    amazon_resolver = AmazonResolver(
        product_id=PRODUCT_ID,
        product_url=AMAZON_URL,
        product_title=PRODUCT_TITLE
    )
    products.append(amazon_resolver.resolve())
    
    # Check Newegg
    newegg_resolver = NeweggResolver(
        product_id=PRODUCT_ID,
        product_url=NEWEGG_URL,
        product_title=PRODUCT_TITLE
    )
    products.append(newegg_resolver.resolve())
    
    return products

def publish_to_discord(products: list[Product]) -> None:
    """
    Publishes product information to Discord.
    """
    # Retrieve webhook from Parameter Store
    discord_webhook_url_arn = os.getenv('DISCORD_WEBHOOK_URL_ARN')
    discord_webhook_url = ssm_accessor.retrieve_parameter(discord_webhook_url_arn)
    
    for product in products:
        if product.is_available:
            message = (
                f"🎮 **{product.title}**\n"
                f"💰 Price: ${product.price:.2f}\n"
                f"🏪 Store: {product.store}\n"
                f"🔗 {product.url}"
            )
            discord_publish(discord_webhook_url, message)

def handle(event, context):
    """
    Entry point for the Lambda function.
    """
    products = find_product_availability()
    previous_amazon = dynamodb_accessor.query_item(PRODUCT_ID, Store.AMAZON.name)
    previous_newegg = dynamodb_accessor.query_item(PRODUCT_ID, Store.NEWEGG.name)

    for product in products:
        if product.store == Store.AMAZON.name:
            if previous_amazon is None:
                print("First run for this product on Amazon - save to DynamoDB")
                dynamodb_accessor.put_item(product)
                # Only publish if product is in stock
                if product.is_available:
                    publish_to_discord([product])
                    print("Case 2: Product is initially in stock on Amazon. Published to Discord")
                else:
                    print("Case 1: Product is initially out of stock on Amazon. Do not publish to Discord")
            else:
                if product.is_available and not previous_amazon.is_available:
                    print("Case 6: Product was previously out of stock on Amazon. Save to DB and publish to Discord")
                    dynamodb_accessor.put_item(product)
                    publish_to_discord([product])
                elif product.is_available and previous_amazon.is_available:
                    print("Case 3: Product was already in stock on Amazon. Do not save to DB or publish")
                elif not product.is_available and previous_amazon.is_available:
                    print("Case 4: Product was previously in stock on Amazon. Save to DB, do not publish.")
                    dynamodb_accessor.put_item(product)
                else:
                    print("Case 5: Product was already out of stock on Amazon. Do not save to DB or publish")
        elif product.store == Store.NEWEGG.name:
            if previous_newegg is None:
                print("First run for this product on Newegg - save to DynamoDB")
                dynamodb_accessor.put_item(product)
                # Only publish if product is in stock
                if product.is_available:
                    publish_to_discord([product])
                    print("Case 2: Product is initially in stock on Newegg. Published to Discord")
                else:
                    print("Case 1: Product is initially out of stock on Newegg. Do not publish to Discord")
            else:
                if product.is_available and not previous_newegg.is_available:
                    print("Case 6: Product was previously out of stock on Newegg. Save to DB and publish to Discord")
                    dynamodb_accessor.put_item(product)
                    publish_to_discord([product])
                elif product.is_available and previous_newegg.is_available:
                    print("Case 3: Product was already in stock on Newegg. Do not save to DB or publish")
                elif not product.is_available and previous_newegg.is_available:
                    print("Case 4: Product was previously in stock on Newegg. Save to DB, do not publish.")
                    dynamodb_accessor.put_item(product)
                else:
                    print("Case 5: Product was already out of stock on Newegg. Do not save to DB or publish")
