# PC Parts Price Tracker

A serverless application that tracks PC component prices from various retailers and sends notifications through Discord when prices change or items become available.

## Features

- 🤖 Automated price tracking using AWS Lambda
- 📊 Price history storage in DynamoDB
- 🔔 Real-time Discord notifications
- ⚡ Serverless architecture for scalability
- 🛍️ Multi-retailer support (currently Canada Computers)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/kaldun-tech/pc-parts-scraper.git
cd pc-parts-scraper
```

2. Install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r lambda\requirements.txt
playwright install  # Install browser binaries for web scraping
```

3. Configure environment variables:
- Create a `.env` file in the root directory with the following variables:
```bash
# Discord webhook URL for notifications
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# AWS credentials (if not using AWS CLI profile)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_preferred_region
```

The environment variables are loaded using python-dotenv in both the CDK stack and Lambda function. If you're using the AWS CLI with a configured profile, you don't need to set the AWS credentials in the `.env` file.

4. Deploy with CDK:
```bash
cdk deploy
```

## Development

- Python code is formatted using Black
- All new code must include type hints
- Tests are located in the `tests` directory
- Lambda function code is in the `lambda` directory
- CDK infrastructure code is in `pc_parts_scraper`

## Documentation

Additional documentation can be found in the `.notes` directory:
- [Project Overview](.notes/project_overview.md)
- [Task List](.notes/task_list.md)
- [Directory Structure](.notes/directory_structure.md)

## Contributing

Contributions are welcome! Please ensure you:
1. Include type hints in Python code
2. Format code with Black
3. Update documentation as needed
4. Add tests for new features
