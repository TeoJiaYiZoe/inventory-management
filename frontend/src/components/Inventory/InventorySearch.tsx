import React from "react";
import { Form, DatePicker, Select, Button, Space } from "antd";
import { SearchFormValues } from "../../types";

interface Props {
  form: any;
  onSearch: (values: SearchFormValues) => void;
  categories: string[];
  loading: boolean;
}

export const InventorySearch: React.FC<Props> = ({
  form,
  onSearch,
  categories,
  loading,
}) => {
  return (
    <Form<SearchFormValues> form={form} onFinish={onSearch} layout="inline">
      <Form.Item name="dateRange" label="Date Range">
        <DatePicker.RangePicker showTime />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Search
        </Button>
      </Form.Item>
      <Form.Item name="category" label="Category">
        <Select
          placeholder="Select category"
          style={{ width: 200 }}
          allowClear
          options={categories.map((cat) => ({ value: cat, label: cat }))}
        />
      </Form.Item>
    </Form>
  );
};
