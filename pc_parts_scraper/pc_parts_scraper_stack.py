from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    aws_events as events,
    Duration,
)
from constructs import Construct
from aws_cdk.aws_ecr_assets import DockerImageAsset
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
        # Create an ECR repo for docker image
        stock_notifier_docker_image = DockerImageAsset(
            self,
            "StockNotifierDockerImage",
            directory="./lambda",
            file="Dockerfile"
        )
        # Lambda function
        stock_notifier_lambda = _lambda.DockerImageFunction(
            self,
            "StockNotifierLambda",
            function_name="StockNotifierLambda",
            memory_size=2048,
            timeout=Duration.seconds(600),
            environment={ "DISCORD_WEBHOOK_URL_ARN": string_param.parameter_arn},
            code=_lambda.DockerImageCode.from_ecr(
                repository=stock_notifier_docker_image.repository,
                tag_or_digest=stock_notifier_docker_image.image_tag,
            )
        )
        # Stock DynamoDB table
        stock_dynamo_table = _dynamodb.Table(
            self,
            "StockTable",
            table_name="StockTable",
            partition_key=_dynamodb.Attribute(
                name="PartId",
                type=_dynamodb.AttributeType.STRING
            ),
            sort_key=_dynamodb.Attribute(
                name="StoreId",
                type=_dynamodb.AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST
        )
        # CloudWatch event each minute
        one_minute_event_rule = events.Rule(
            self,
            "MinuteRule",
            schedule=events.Schedule.cron(
                minute="0", # TODO - Change to *
                hour="0", # TODO - Change to *
                month="*",
                day="*",
                year="*"
            )
        )
