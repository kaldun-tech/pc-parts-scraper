from product_resolvers.cc_resolver import CanadaComputersResolver
import os
from dotenv import load_dotenv
from aws_accessors import ssm_accessor
from discord import discord_publisher

# Load environment variables from .env file
load_dotenv()

PRODUCT_ID = "GSKILL RipJaws 32GB"
PRODUCT_URL = "https://www.canadacomputers.com/en/desktop-memory/99478/g-skill-ripjaws-v-32gb-2x16gb-ddr4-3200mhz-cl16-udimm-f4-3200c16d-32gvk.html"
PRODUCT_TITLE = "GSKILL RipJaws 32GB"

def handle(event, context):
    # Find product availability
    resolver = CanadaComputersResolver(
        product_id=PRODUCT_ID,
        product_url=PRODUCT_URL,
        product_title=PRODUCT_TITLE
    )
    product = resolver.resolve()
    print(product)

    # Send notification to Discord
    # Read the parameter from Parameter Store
    discord_webhook_url_arn = os.getenv('DISCORD_WEBHOOK_URL_ARN')
    print(f"Retrieved ARN from env: {discord_webhook_url_arn}")
    # Read off the parameter value to retrieve webhook
    discord_webhook_url = ssm_accessor.retrieve_parameter(discord_webhook_url_arn)
    print(f"Retrieved webhook URL: {discord_webhook_url}")
    # Publish to Discord
    discord_publisher.publish(discord_webhook_url, product)
    print("Published to Discord")

handle(None, None)
