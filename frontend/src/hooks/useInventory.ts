import { useState } from 'react';
import { message } from 'antd';
import { inventoryServiceAxios } from '../axios/inventoryServiceAxios';
import { CreateFormValues, Item, QueryParams, Stats } from '../types';

export const useInventory = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [stats, setStats] = useState<Stats>({ 
    totalItems: 0, 
    totalValue: 0 
  });
  const [loading, setLoading] = useState(false);

  const fetchItems = async (params?: QueryParams) => {
    try {
      setLoading(true);
      const { items, stats } = await inventoryServiceAxios.getItems(params);
      setItems(items);
      setStats(stats);
    } catch (error) {
      message.error('Failed to load items. Please try again.');
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllCategories = async () => {
    try {
      const categories = await inventoryServiceAxios.getCategories();
      setCategories(categories);
    } catch (error) {
      message.error('Failed to load categories.');
      console.error('Error fetching categories:', error);
    }
  };

const createItem = async (values: CreateFormValues) => {
  try {
    setLoading(true);
    const newItem = await inventoryServiceAxios.createItem(values);
    setItems(prev => [...prev, newItem]);
    await fetchAllCategories();
    return true;
  } catch (error) {
    console.error('Error creating item:', error);
    message.error('Failed to create item. Please check the data and try again.');
    return false;
  } finally {
    setLoading(false);
  }
};

const updateItemPrice = async (id: string, price: number) => {
  try {
    setLoading(true);
    const updatedItem = await inventoryServiceAxios.updateItemPrice(id, { price });
    setItems(prev => 
      prev.map(item => item.id === id ? updatedItem : item)
    );
    return true;
  } catch (error) {
    console.error('Error updating price:', error);
    message.error('Failed to update price. Please check the value and try again.');
    return false;
  } finally {
    setLoading(false);
  }
};

  return {
    items,
    categories,
    stats,
    loading,
    fetchItems,
    fetchAllCategories,
    createItem,
    updateItemPrice
  };
};