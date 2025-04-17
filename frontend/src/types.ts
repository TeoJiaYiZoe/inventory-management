import { Dayjs } from "dayjs";

export interface Item {
  id: string;
  name: string;
  category: string;
  price: number;
  last_updated_dt: string;
}

export interface QueryParams {
  category?: string;
  dt_from?: string;
  dt_to?: string;
}

export interface Stats {
  totalItems: number;
  totalValue: number;
}

export interface SearchFormValues {
  category?: string;
  dateRange?: [Dayjs, Dayjs];
}

export interface CreateFormValues {
  name: string;
  category: string;
  price: number;
}

export interface EditFormValues {
  price: number;
}