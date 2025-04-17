import axios from 'axios';
import { 
  Item, 
  QueryParams, 
  CreateFormValues, 
  EditFormValues,
  Stats 
} from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const transformItem = (item: any): Item => ({
  id: item.id,
  name: item.item_name || item.name,
  category: item.category,
  price: parseFloat(item.price.toString()),
  last_updated_dt: item.last_updated_dt
});

export const inventoryServiceAxios = {
  async getItems(params?: QueryParams): Promise<{ items: Item[]; stats: Stats }> {
    const response = await api.get('/items', { params });
    
    const items: Item[] = response.data.items.map(transformItem);
    
    return {
      items,
      stats: {
        totalItems: items.length,
        totalValue: response.data.total_price || 
                   items.reduce((sum: number, item: Item) => sum + item.price, 0)
      }
    };
  },

  async getCategories(): Promise<string[]> {
    const response = await api.get('/items');
    const items: Item[] = response.data.items.map(transformItem);
    return Array.from(new Set(items.map((item: Item) => item.category)));
  },

  async createItem(values: CreateFormValues): Promise<Item> {
    const response = await api.post('/items', values);
    return transformItem(response.data);
  },

  async updateItemPrice(id: string, values: EditFormValues): Promise<Item> {
    const response = await api.put(`/items/${id}/price`, values);
    return transformItem(response.data);
  },
};

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);