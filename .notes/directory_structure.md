# Directory Structure

pc-parts-scraper/
├── .notes/                     # Project documentation
│   ├── project_overview.md     # Project description and goals
│   ├── task_list.md           # Current and planned tasks
│   └── directory_structure.md  # This file
├── lambda/                     # Lambda function code
│   ├── aws_accessors/         # AWS service interaction modules
│   ├── discord/               # Discord integration
│   ├── models/                # Data models
│   ├── product_resolvers/     # Product resolution logic
│   ├── handler.py            # Main Lambda handler
│   ├── Dockerfile            # Container configuration
│   └── requirements.txt      # Lambda-specific dependencies
├── pc_parts_scraper/         # CDK infrastructure code
├── tests/                    # Test files
├── app.py                    # CDK app entry point
├── cdk.json                  # CDK configuration
├── requirements.txt          # Project dependencies
└── requirements-dev.txt      # Development dependencies

## Directory Descriptions

### lambda/
Contains the Lambda function code and its dependencies.

#### aws_accessors/
Modules for interacting with AWS services.

#### discord/
Discord bot integration code.

#### models/
Data models and schemas.

#### product_resolvers/
Logic for resolving and processing product data.

### pc_parts_scraper/
Contains the AWS CDK infrastructure code that defines the cloud resources.

### tests/
Unit tests and integration tests.

### Root Files
- `app.py`: The entry point for the CDK application
- `cdk.json`: CDK configuration file
- `requirements.txt`: Project-level Python dependencies
- `requirements-dev.txt`: Development dependencies
