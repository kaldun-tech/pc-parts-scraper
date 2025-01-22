import boto3
from botocore.exceptions import ClientError
import os

# Get profile from environment variable or use default
aws_profile = os.getenv('AWS_PROFILE', 'default')
print(f"Using AWS profile: {aws_profile}")

# Create a session using your profile
session = boto3.Session(profile_name=aws_profile)
ssm_client = session.client('ssm', region_name='us-east-1')

def retrieve_parameter(parameter: str) -> str:
    try:
        response = ssm_client.get_parameter(Name=parameter, WithDecryption=True)
        value = response['Parameter']['Value']
        print(f"Retrieved parameter {parameter} with value {value}")
        return value
    except ClientError as e:
        if e.response['Error']['Code'] == 'ParameterNotFound':
            print(f"Parameter {parameter} not found")
        else:
            print(f"Error retrieving parameter {parameter}: {e}")
        raise e
