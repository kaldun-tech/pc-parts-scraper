#!/usr/bin/env python3
import os

import aws_cdk as cdk
from pc_parts_scraper.pc_parts_scraper_stack import PcPartsScraperStack


app = cdk.App()
PcPartsScraperStack(app, "PcPartsScraperStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()
