import React from "react";
import { Form, Button, Select, DatePicker } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { SearchFormValues } from "../../types";

const { RangePicker } = DatePicker;

interface Props {
  onSearch: (values: SearchFormValues) => void;
  categories: string[];
  loading: boolean;
}

export const InventorySearch: React.FC<Props> = ({
  onSearch,
  categories,
  loading,
}) => {
  const [form] = Form.useForm<SearchFormValues>();

  return (
    <Form form={form} onFinish={onSearch} layout="inline">
      <Form.Item name="dateRange" label="Date Range">
        <RangePicker showTime format="YYYY-MM-DD HH:mm:ss" />
      </Form.Item>
      <Form.Item name="category" label="Category">
        <Select
          placeholder="Filter by category"
          style={{ width: 200 }}
          allowClear
          options={categories.map((category) => ({
            label: category,
            value: category,
          }))}
        />
      </Form.Item>
      <Form.Item>
        <Button
          type="primary"
          htmlType="submit"
          icon={<SearchOutlined />}
          loading={loading}
        >
          Search
        </Button>
      </Form.Item>
    </Form>
  );
};
