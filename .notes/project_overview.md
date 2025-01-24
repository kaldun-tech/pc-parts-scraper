# PC Parts Scraper - Project Overview

## Purpose
A serverless price tracking solution that monitors PC component prices from various retailers and notifies users through Discord when prices change or items become available.

## Core Features
- Automated price tracking using AWS Lambda
- Discord notifications for price changes and availability
- Multi-retailer support (currently Canada Computers)
- DynamoDB-based data persistence

## Technology Stack
- Python with type hints
- AWS Lambda for serverless execution
- AWS DynamoDB for data storage
- Discord for notifications
- AWS CDK for infrastructure as code

## Project Goals
1. Track PC component prices across major retailers
2. Provide real-time Discord notifications for price changes
3. Scale efficiently using serverless architecture
4. Support multiple retailers and product types

## Development Guidelines
- Use Python type hints for all new code
- Format code using Black
- Follow AWS Lambda best practices
- Maintain comprehensive documentation
- Write unit tests for new features

## Current Implementation
- Tracks specific PC components (e.g., RAM modules)
- Supports Canada Computers as initial retailer
- Uses Discord webhooks for notifications
- Leverages DynamoDB for price history
