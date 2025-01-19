from aws_cdk import (
    Stack,
    aws_ssm as ssm,
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()

class PcPartsScraperStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ParameterStore details for Discord webhook URL
        discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        string_param = ssm.StringParameter(
            self,
            "DiscordWebhookUrl",
            parameter_name="DISCORD_WEBHOOK_URL",
            string_value=discord_webhook_url,
            description="Discord Webhook URL String",
            tier=ssm.ParameterTier.STANDARD
        )
