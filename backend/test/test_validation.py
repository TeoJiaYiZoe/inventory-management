import pytest
from pydantic import ValidationError
from core.models import ItemCreate

def test_item_create_invalid_type():
    with pytest.raises(ValidationError):
        ItemCreate(name=123, category="food", price=10.0)

def test_item_validation(client):
    invalid_items = [
        {"name": "", "category": "test", "price": 10.99},
        {"name": "test", "category": "", "price": 10.99},
        {"name": "test", "category": "test", "price": 0},
    ]
    for item in invalid_items:
        response = client.post("/items/", json=item)
        assert response.status_code == 422

def test_price_update_validation(client,TEST_ITEM):
    invalid_prices = [{"price": 0}, {"price": -1.99}]
    for price in invalid_prices:
        response = client.put(f"/items/{TEST_ITEM['id']}/price", json=price)
        assert response.status_code == 422