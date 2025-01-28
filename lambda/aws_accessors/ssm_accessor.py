import boto3
from botocore.exceptions import ClientError
import os
from .aws_session import AWSSession, handle_aws_error

# Create a session using Lambda's IAM role credentials
session = boto3.Session()

ssm_client = AWSSession.get_client('ssm')

@handle_aws_error('SSM parameter retrieval')
def retrieve_parameter(parameter: str) -> str:
    response = ssm_client.get_parameter(Name=parameter, WithDecryption=True)
    value = response['Parameter']['Value']
    print(f"Retrieved parameter {parameter}")
    return value
