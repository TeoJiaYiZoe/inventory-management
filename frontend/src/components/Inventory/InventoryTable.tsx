import React from "react";
import { Table, Button } from "antd";
import { EditOutlined } from "@ant-design/icons";
import { Item } from "../../types";

interface Props {
  items: Item[];
  loading: boolean;
  onEdit: (item: Item) => void;
}

export const InventoryTable: React.FC<Props> = ({ items, loading, onEdit }) => {
  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      sorter: (a: Item, b: Item) => a.name.localeCompare(b.name),
    },
    {
      title: "Category",
      dataIndex: "category",
      key: "category",
      sorter: (a: Item, b: Item) => a.category.localeCompare(b.category),
    },
    {
      title: "Price (SGD)",
      dataIndex: "price",
      key: "price",
      render: (price: number) => `SGD ${price.toFixed(2)}`,
      sorter: (a: Item, b: Item) => a.price - b.price,
    },
    {
      title: "Action",
      key: "action",
      render: (_: any, record: Item) => (
        <Button
          type="link"
          icon={<EditOutlined />}
          onClick={() => onEdit(record)}
        >
          Edit Price
        </Button>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={items}
      rowKey="id"
      style={{ marginTop: "16px" }}
      loading={loading}
    />
  );
};
