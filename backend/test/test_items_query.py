import pytest
from datetime import datetime, timedelta
from urllib.parse import quote
from test.constants import SGT

@pytest.mark.asyncio
async def test_query_items_no_filters(mock_inventory_service, create_test_items, client):
    test_items = create_test_items(3)
    mock_inventory_service.query_items.return_value = test_items
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3

@pytest.mark.asyncio
async def test_query_items_with_category_filter(mock_inventory_service, create_test_items, client):
    test_items = create_test_items(2)
    mock_inventory_service.query_items.return_value = test_items
    response = client.get("/items/?category=test")
    assert response.status_code == 200
    mock_inventory_service.query_items.assert_called_once_with(
        dt_from=None, dt_to=None, category="test"
    )

@pytest.mark.asyncio
async def test_query_items_category_filter(mock_inventory_service, client):
    mock_inventory_service.query_items_paginated.return_value = {
        "items": [], "count": 0, "page": 1, "limit": 10
    }
    response = client.get("/query-items/?category=stationery")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_query_items_with_price_filter(mock_inventory_service, create_test_items, client):
    test_items = create_test_items(3)
    mock_inventory_service.query_items_paginated.return_value = {
        "items": test_items["items"], "count": 3, "page": 1, "limit": 10
    }
    response = client.get("/query-items/?price_min=10&price_max=20")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_date_filtering_within_range(mock_inventory_service, create_test_item_with_dt, client):
    test_item = create_test_item_with_dt(hours_ago=12)
    mock_inventory_service.query_items.return_value = {
        "items": [test_item], "total_price": test_item["price"]
    }
    now = datetime.now(SGT)
    dt_from = (now - timedelta(hours=24)).astimezone(SGT).isoformat(sep="T")
    dt_to = now.astimezone(SGT).isoformat(sep="T")
    response = client.get(f"/items/?dt_from={quote(dt_from)}&dt_to={quote(dt_to)}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_query_items_pagination(mock_inventory_service, create_test_items, client):
    test_items = create_test_items(15)
    mock_inventory_service.query_items_paginated.return_value = {
        "items": test_items["items"][5:10], "count": 15, "page": 2, "limit": 5
    }
    response = client.get("/query-items/?page=2&limit=5")
    assert response.status_code == 200