from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List

class ItemCreate(BaseModel):
    item_name: str = Field(..., alias="name", min_length=1)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

    @field_validator('item_name', 'category')
    @classmethod
    def convert_to_lowercase(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Value must be a string")
        return v.lower()

class PriceUpdate(BaseModel):
    price: float = Field(..., gt=0)

class ItemResponse(BaseModel):
    id: str
    name: str = Field(..., alias="item_name")
    category: str
    price: float
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "item_name": "Test Item",
                "category": "test Category",
                "price": 19.99,
                "last_updated_dt": "2025-01-01T00:00:00+08:00"
            }
        }
    )

class QueryResponse(BaseModel):
    items: List[ItemResponse]
    count: int
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1, le=100)

class DeleteResponse(BaseModel):
    status: str
    deleted_id: str