import sys
import os
from decimal import Decimal
import pytest
from unittest.mock import patch, MagicMock

# Add project root and lambda to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
lambda_path = os.path.join(project_root, 'lambda')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if lambda_path not in sys.path:
    sys.path.insert(0, lambda_path)

from handler import handle
from models.product import Product
from models.store import Store

@pytest.fixture
def mock_product():
    return Product(
        id="NVIDIA-RTX-3090TI-FE",
        name="NVIDIA GeForce RTX 3090 TI Founders Edition",
        price=Decimal('1999.99'),
        url="https://amazon.com/test",
        store=Store.AMAZON,
        in_stock=True
    )

@patch('handler.find_product_availability')
@patch('handler.dynamodb_accessor')
@patch('handler.publish_to_discord')
def test_new_product_in_stock_amazon(mock_discord, mock_dynamo, mock_find, mock_product):
    # Arrange
    mock_find.return_value = [mock_product]
    mock_dynamo.query_item.return_value = None  # No previous record

    # Act
    handle(None, None)

    # Assert
    mock_dynamo.put_item.assert_called_once_with(mock_product)
    mock_discord.assert_called_once_with([mock_product])
