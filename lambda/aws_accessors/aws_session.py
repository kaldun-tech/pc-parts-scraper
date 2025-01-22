import boto3
from botocore.exceptions import ClientError
import os
from typing import Any

class AWSSession:
    _instance = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AWSSession, cls).__new__(cls)
            # Get profile from environment variable or use default
            aws_profile = os.getenv('AWS_PROFILE', 'default')
            cls._session = boto3.Session(profile_name=aws_profile)
        return cls._instance

    @classmethod
    def get_session(cls) -> boto3.Session:
        if cls._instance is None:
            cls()
        return cls._session

    @classmethod
    def get_client(cls, service: str) -> Any:
        return cls.get_session().client(service, region_name='us-east-1')

    @classmethod
    def get_resource(cls, service: str) -> Any:
        return cls.get_session().resource(service, region_name='us-east-1')

def handle_aws_error(operation: str):
    """Decorator for handling AWS ClientErrors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientError as e:
                print(f"AWS Error during {operation}: {e.response['Error']['Message']}")
                raise e
        return wrapper
    return decorator
