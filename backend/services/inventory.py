from uuid import uuid4
from decimal import Decimal
from fastapi import HTTPException
import logging
from core.database import get_db
from core.models import ItemCreate, ItemResponse, PriceUpdate, QueryResponse
from typing import Optional
from utils.helpers import format_price, get_sgt_time, parse_datetime

logger = logging.getLogger(__name__)

class InventoryService:
    def __init__(self):
        self.db = get_db()
        self.table = self.db.Table('Inventory')

    async def create_or_update_item(self, item: ItemCreate) -> dict:
        try:
            response = self.table.query(
                IndexName='NameIndex',
                KeyConditionExpression='item_name = :name',
                ExpressionAttributeValues={':name': item.item_name}
            )

            items = response['Items'] if 'Items' in response else []
            now = get_sgt_time()
            price_str = format_price(item.price)
            
            if items:
                item_id = items[0]['id']
                self.table.update_item(
                    Key={'id': item_id},
                    UpdateExpression="SET price = :price, last_updated_dt = :dt",
                    ExpressionAttributeValues={
                        ":price": price_str,
                        ":dt": now
                    }
                )
                logger.info(f"Updated item {item_id} with new price {price_str}")
            else:
                item_id = str(uuid4())
                self.table.put_item(Item={
                    'id': item_id,
                    'item_name': item.item_name,
                    'category': item.category,
                    'price': price_str,
                    'last_updated_dt': now
                })
                logger.info(f"Created new item {item_id} with price {price_str}")
            
            return {"id": item_id}
        
        except Exception as e:
            logger.error(f"Error in create_or_update_item: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def query_items(
        self,
        dt_from: Optional[str] = None,
        dt_to: Optional[str] = None,
        category: Optional[str] = None
    ) -> dict:
        try:
            if category:
                category = category.lower()
                
            dt_from_parsed = parse_datetime(dt_from) if dt_from else None
            dt_to_parsed = parse_datetime(dt_to) if dt_to else None
            
            logger.info(f"Querying items with filters - dt_from: {dt_from_parsed}, dt_to: {dt_to_parsed}, category: {category}")

            scan_params = {}
            if category:
                scan_params['FilterExpression'] = 'category = :cat'
                scan_params['ExpressionAttributeValues'] = {':cat': category}
            
            items = []
            last_key = None
            
            # Paginated scan
            while True:
                if last_key:
                    scan_params['ExclusiveStartKey'] = last_key
                
                response = self.table.scan(**scan_params)
                items_list = response['Items'] if 'Items' in response else []
                items.extend(items_list)
                
                last_key = response.get('LastEvaluatedKey')
                if not last_key:
                    break
            
            # Filter items with strict comparisons
            filtered = []
            total = Decimal('0')
            
            for item in items:
                try:
                    if not all(k in item for k in ['id', 'item_name', 'category', 'price', 'last_updated_dt']):
                        logger.warning(f"Skipping incomplete item: {item.get('id')}")
                        continue
                    
                    item_dt = parse_datetime(item['last_updated_dt'])
                    include = True
                    
                    logger.debug(f"Comparing: {item_dt} to range {dt_from_parsed} - {dt_to_parsed}")
                    
                    if dt_from_parsed and item_dt < dt_from_parsed:
                        include = False
                        logger.debug("Excluded - before start date")
                    if dt_to_parsed and item_dt > dt_to_parsed:
                        include = False
                        logger.debug("Excluded - after end date")
                    
                    if include:
                        filtered.append(ItemResponse(
                            id=item['id'],
                            item_name=item['item_name'],
                            category=item['category'],
                            price=float(item['price'])
                        ).model_dump(by_alias=True))
                        total += Decimal(item['price'])
                        logger.debug("Included")
                    else:
                        logger.debug(f"Excluded item {item['id']} at {item_dt}")
                except Exception as e:
                    logger.error(f"Error processing item {item.get('id')}: {str(e)}")
                    continue
            
            logger.info(f"Returning {len(filtered)} filtered items")
            return {
                "items": filtered,
                "total_price": format_price(total)
            }
            
        except Exception as e:
            logger.error(f"Error in query_items: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    # Only for Backend API
    async def query_items_paginated(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        page: int = 1,
        limit: int = 10,
        sort_field: str = "name",
        sort_order: str = "asc"
    ) -> QueryResponse:
        try:
            logger.info(f"Querying items with filters - name: {name}, category: {category}, price range: {price_min}-{price_max}")
            
            scan_params = {}
            filter_expressions = []
            expression_attrs = {}
            
            # Apply filters
            if name:
                name = name.lower()
                filter_expressions.append("contains(item_name, :name)")
                expression_attrs[":name"] = name
            if category:
                category = category.lower()
                filter_expressions.append("category = :category")
                expression_attrs[":category"] = category
            
            if filter_expressions:
                scan_params['FilterExpression'] = " AND ".join(filter_expressions)
                scan_params['ExpressionAttributeValues'] = expression_attrs
            
            items = []
            last_key = None
            while True:
                if last_key:
                    scan_params['ExclusiveStartKey'] = last_key
                response = self.table.scan(**scan_params)
                items_list = response['Items'] if 'Items' in response else []
                items.extend(items_list)
                
                last_key = response.get('LastEvaluatedKey')
                if not last_key:
                    break
            
            # Apply price filter
            if price_min is not None and price_max is not None:
                items = [
                    item for item in items
                    if price_min <= float(item['price']) <= price_max
                ]
            
            # Apply sorting
            reverse_sort = sort_order == "desc"
            items.sort(
                key=lambda x: (
                    float(x['price']) if sort_field == "price" 
                    else x.get(sort_field, "")
                ),
                reverse=reverse_sort
            )
            
            # Apply pagination
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_items = items[start_idx:end_idx]
            
            # Convert to response
            result_items = [
                ItemResponse(
                    id=item['id'],
                    item_name=item['item_name'],
                    category=item['category'],
                    price=float(item['price'])
                )
                for item in paginated_items
            ]
            
            logger.info(f"Returning {len(result_items)} items (page {page} of {len(items)//limit + 1})")
            return QueryResponse(
                items=result_items,
                count=len(items),
                page=page,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error in query_items_paginated: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def update_item_price(self, item_id: str, price_update: PriceUpdate) -> dict:
        try:
            logger.info(f"Updating price for item {item_id} to {price_update.price}")
            
            response = self.table.get_item(Key={'id': item_id})
            item = response.get("Item")
            if item is None:
                logger.warning(f"Item not found: {item_id}")
                raise HTTPException(status_code=404, detail="Item not found")
            
            now = get_sgt_time()
            price_str = format_price(price_update.price)
            
            self.table.update_item(
                Key={'id': item_id},
                UpdateExpression="SET price = :price, last_updated_dt = :dt",
                ExpressionAttributeValues={
                    ":price": price_str,
                    ":dt": now
                }
            )
            
            logger.info(f"Successfully updated price for item {item_id}")
            return {"status": "success", "updated_price": price_str}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    async def delete_item(self, item_id: str) -> dict:
        try:
            response = self.table.get_item(
                Key={'id': item_id}
            )
            
            if 'Item' not in response:
                logger.error(f"Item {item_id} not found")
                raise HTTPException(status_code=404, detail="Item not found")
            
            self.table.delete_item(
                Key={'id': item_id}
            )
            
            logger.info(f"Deleted item {item_id}")
            return {"status": "success", "deleted_id": item_id}
        
        except HTTPException:
            raise 
        except Exception as e:
            logger.error(f"Error in delete_item: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))