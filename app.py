#!/usr/bin/env python3
import os
from dotenv import load_dotenv

import aws_cdk as cdk
from pc_parts_scraper.pc_parts_scraper_stack import PcPartsScraperStack

# Load environment variables from .env file
load_dotenv()

app = cdk.App()
PcPartsScraperStack(app, "PcPartsScraperStack",
    # The environment will be determined by the AWS profile
    # specified either in AWS_PROFILE environment variable
    # or via --profile in the CDK command
    env=cdk.Environment()
)

app.synth()
