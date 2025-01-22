import boto3
from botocore.exceptions import ClientError
import os
from .aws_session import AWSSession, handle_aws_error

# Get profile from environment variable or use default
aws_profile = os.getenv('AWS_PROFILE', 'default')
print(f"Using AWS profile: {aws_profile}")

# Create a session using your profile
session = boto3.Session(profile_name=aws_profile)

ssm_client = AWSSession.get_client('ssm')

@handle_aws_error('SSM parameter retrieval')
def retrieve_parameter(parameter: str) -> str:
    response = ssm_client.get_parameter(Name=parameter, WithDecryption=True)
    value = response['Parameter']['Value']
    print(f"Retrieved parameter {parameter}")
    return value
