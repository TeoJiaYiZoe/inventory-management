import axios from 'axios';
import { 
  Item, 
  QueryParams, 
  CreateFormValues, 
  EditFormValues,
  Stats,
  DeleteResponse 
} from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const transformItem = (item: any): Item => ({
  id: item.id,
  name: item.item_name || item.name || '',
  category: item.category || '',
  price: item.price ? parseFloat(item.price.toString()) : 0,
  last_updated_dt: item.last_updated_dt || new Date().toISOString()
});

export const inventoryServiceAxios = {
  async getItems(params?: QueryParams): Promise<{ items: Item[]; stats: Stats }> {
    try {
      const response = await api.get('/items/', { params });
      
      const items: Item[] = response.data.items?.map(transformItem) || [];
      
      return {
        items,
        stats: {
          totalItems: items.length,
          totalValue: response.data.total_price || 
                     items.reduce((sum: number, item: Item) => sum + item.price, 0)
        }
      };
    } catch (error) {
      console.error('Error getting items:', error);
      return { items: [], stats: { totalItems: 0, totalValue: 0 } };
    }
  },

  async getCategories(): Promise<string[]> {
    try {
      const response = await api.get('/items/');
      const items: Item[] = response.data.items?.map(transformItem) || [];
      return Array.from(new Set(items.map((item: Item) => item.category)));
    } catch (error) {
      console.error('Error getting categories:', error);
      return [];
    }
  },

  async createItem(values: CreateFormValues): Promise<Item> {
    try {
      const response = await api.post('/items/', values);
      return transformItem(response.data);
    } catch (error) {
      console.error('Error creating item:', error);
      throw error;
    }
  },

  async updateItemPrice(id: string, values: EditFormValues): Promise<Item> {
    try {
      const response = await api.put(`/items/${id}/price/`, values);
      return transformItem(response.data);
    } catch (error) {
      console.error('Error updating item price:', error);
      throw error;
    }
  },
  async deleteItem(id: string): Promise<DeleteResponse> {
    try {
      const response = await api.delete(`/items/${id}/`);
      return {
        status: 'success',
        deletedId: response.data.deleted_id
      };
    } catch (error) {
      console.error('Error deleting item:', error);
      throw error;
    }
  }
};