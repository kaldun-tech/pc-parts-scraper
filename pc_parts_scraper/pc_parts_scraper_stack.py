from aws_cdk import (
    Duration,
    Stack,
    aws_ssm as ssm,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    aws_events as events,
    aws_events_targets as targets,
    aws_ecr_assets,
    aws_iam as iam,
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
        webhook_param = ssm.StringParameter(
            self,
            "DiscordWebhookUrl",
            parameter_name="DISCORD_WEBHOOK_URL",
            string_value=discord_webhook_url,
            description="Discord Webhook URL String",
            tier=ssm.ParameterTier.STANDARD
        )

        # ParameterStore details for AWS Profile
        aws_profile = os.getenv('AWS_PROFILE', 'default')
        profile_param = ssm.StringParameter(
            self,
            "AWSProfile",
            parameter_name="AWS_PROFILE",
            string_value=aws_profile,
            description="AWS Profile for Lambda Function",
            tier=ssm.ParameterTier.STANDARD
        )
        # Create an ECR repo for docker image
        stock_notifier_docker_image = aws_ecr_assets.DockerImageAsset(
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
            environment={
                "DISCORD_WEBHOOK_URL": discord_webhook_url,  # Pass URL directly
                "DISCORD_WEBHOOK_URL_ARN": webhook_param.parameter_arn,  # Keep ARN for reference
                "AWS_PROFILE": aws_profile,  # Pass profile directly
                "AWS_PROFILE_ARN": profile_param.parameter_arn,  # Keep ARN for reference
            },
            code=_lambda.DockerImageCode.from_ecr(
                repository=stock_notifier_docker_image.repository,
                tag_or_digest=stock_notifier_docker_image.image_tag,
            )
        )
        # Grant SSM permissions
        webhook_param.grant_read(stock_notifier_lambda)
        profile_param.grant_read(stock_notifier_lambda)

        # Grant additional permissions if needed
        stock_notifier_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "ssm:GetParameter",
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query"
                ],
                resources=[
                    webhook_param.parameter_arn,
                    profile_param.parameter_arn,
                    # Add other resource ARNs as needed
                ]
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
            "HourlyRule",
            schedule=events.Schedule.cron(
                minute="0",
                hour="*",
                month="*",
                day="*",
                year="*"
            )
        )
        # Connects Lambda to CloudWatch event
        stock_notifier_function = targets.LambdaFunction(stock_notifier_lambda)
        one_minute_event_rule.add_target(stock_notifier_function)
        # Give Lambda the permissions to read and write to DynamoDB
        stock_dynamo_table.grant_read_write_data(stock_notifier_lambda)
        # Give Lambda the permissions to pull images from ECR
        stock_notifier_docker_image.repository.grant_pull(stock_notifier_lambda)
