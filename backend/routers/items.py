from typing import Optional
from fastapi import APIRouter
from services.inventory import InventoryService
from core.models import ItemCreate, PriceUpdate, QueryResponse, DeleteResponse

router = APIRouter()
service = InventoryService()

@router.post("/items/", response_model=dict)
async def create_or_update_item(item: ItemCreate):
    return await service.create_or_update_item(item)

@router.get("/items/", response_model=dict)
async def query_items(
    dt_from: Optional[str] = None,
    dt_to: Optional[str] = None,
    category: Optional[str] = None
):
    return await service.query_items(dt_from=dt_from,
        dt_to=dt_to,
        category=category)

@router.get("/query-items/", response_model=QueryResponse)
async def query_items_paginated(
    name: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    page: int = 1,
    limit: int = 10,
    sort_field: str = "name",
    sort_order: str = "asc"
):      
    return await service.query_items_paginated(
        name=name, category=category, price_min=price_min, price_max=price_max, 
        page=page, limit=limit, sort_field=sort_field, sort_order=sort_order
    )

@router.put("/items/{item_id}/price", response_model=dict)
async def update_item_price(item_id: str, price_update: PriceUpdate):
    return await service.update_item_price(item_id, price_update)

@router.delete("/items/{item_id}", response_model=DeleteResponse)
async def delete_item(item_id: str):
    return await service.delete_item(item_id)