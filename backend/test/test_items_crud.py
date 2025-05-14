import pytest
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_create_or_update_item_new(mock_inventory_service, client):
    mock_inventory_service.create_or_update_item.return_value = {"id": "123e4567-e89b-12d3-a456-426614174100"}
    response = client.post("/items/", json={
        "name": "new item",
        "category": "new category",
        "price": 29.99
    })
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_create_or_update_item_existing(mock_inventory_service, client, TEST_ITEM):
    mock_inventory_service.create_or_update_item.return_value = {"id": TEST_ITEM["id"]}
    response = client.post("/items/", json={
        "name": TEST_ITEM["name"],
        "category": TEST_ITEM["category"],
        "price": 25.99
    })
    assert response.status_code == 200
    assert response.json()["id"] == TEST_ITEM["id"]

@pytest.mark.asyncio
async def test_create_or_update_item_500(mock_inventory_service, client):
    async def raise_exception(*args, **kwargs):
        raise HTTPException(status_code=500, detail="Simulated service failure")
    mock_inventory_service.create_or_update_item.side_effect = raise_exception
    response = client.post("/items/", json={
        "name": "TestItem",
        "category": "TestCategory",
        "price": 19.99
    })
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_update_item_price(mock_inventory_service, client, TEST_ITEM):
    mock_inventory_service.update_item_price.return_value = {
        "status": "success",
        "updated_price": "39.99"
    }
    response = client.put(f"/items/{TEST_ITEM['id']}/price", json={"price": 39.99})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@pytest.mark.asyncio
async def test_update_nonexistent_item_price(mock_inventory_service, client):
    mock_inventory_service.update_item_price.side_effect = HTTPException(
        status_code=404, detail="Item not found"
    )
    response = client.put("/items/nonexistent-id/price", json={"price": 39.99})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_item_price_500(mock_inventory_service, client, TEST_ITEM):
    async def raise_exception(*args, **kwargs):
        raise HTTPException(status_code=500, detail="Simulated service error")
    mock_inventory_service.update_item_price.side_effect = raise_exception
    response = client.put(f"/items/{TEST_ITEM['id']}/price", json={"price": 39.99})
    assert response.status_code == 500
    
@pytest.mark.asyncio
async def test_delete_item(mock_inventory_service, client, TEST_ITEM):
    async def mock_delete(item_id):
        return {"status": "success", "deleted_id": item_id}
    
    mock_inventory_service.delete_item = mock_delete
    
    response = client.delete(f"/items/{TEST_ITEM['id']}")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "deleted_id": TEST_ITEM['id']
    }