import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from test.constants import SGT


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def TEST_ITEM():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "test item",
        "category": "test category",
        "price": 19.99,
        "last_updated_dt": datetime.now(SGT).isoformat()
    }
@pytest.fixture
def mock_inventory_service():
    with patch('routers.items.service') as mock_service:
        mock_service.create_or_update_item = AsyncMock()
        mock_service.query_items = AsyncMock()
        mock_service.query_items_paginated = AsyncMock()
        mock_service.update_item_price = AsyncMock()
        yield mock_service

@pytest.fixture
def create_test_items(TEST_ITEM):
    def _create_test_items(count=5, category="test"):
        return {
            "items": [{
                **TEST_ITEM,
                "id": f"test-id-{i}",
                "price": float(f"{10 + i}.99"),
                "last_updated_dt": datetime.now(SGT).isoformat(),
                "category": category
            } for i in range(count)],
            "count": count,
            "total_price": sum(float(f"{10 + i}.99") for i in range(count))
        }
    return _create_test_items

@pytest.fixture
def create_test_item_with_dt():
    def _create_test_item_with_dt(hours_ago=0):
        dt = (datetime.now(SGT) - timedelta(hours=hours_ago)).isoformat()
        return {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "test item",
            "category": "test category",
            "price": 10.99,
            "last_updated_dt": dt
        }
    return _create_test_item_with_dt