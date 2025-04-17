import React, { useState, useEffect } from "react";
import { Button, Form, Modal, Space, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { useInventory } from "./hooks/useInventory";
import { InventoryStats } from "./components/Inventory/InventoryStats";
import { InventoryTable } from "./components/Inventory/InventoryTable";
import { InventorySearch } from "./components/Inventory/InventorySearch";
import { EditForm } from "./components/Inventory/InventoryForms/EditForm";
import { CreateForm } from "./components/Inventory/InventoryForms/CreateForm";
import {
  CreateFormValues,
  EditFormValues,
  Item,
  SearchFormValues,
} from "./types";

const App = () => {
  const {
    items,
    categories,
    stats,
    loading,
    fetchItems,
    fetchAllCategories,
    createItem,
    updateItemPrice,
  } = useInventory();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Item | null>(null);
  const [searchForm] = Form.useForm();

  useEffect(() => {
    fetchItems();
    fetchAllCategories();
  }, []);

  const handleSearch = (values: SearchFormValues) => {
    const params = {
      category: values.category,
      dt_from: values.dateRange?.[0]?.format("YYYY-MM-DD HH:mm:ss"),
      dt_to: values.dateRange?.[1]?.format("YYYY-MM-DD HH:mm:ss"),
    };
    fetchItems(params);
  };

  const handleCreateItem = async (values: CreateFormValues) => {
    try {
      console.log("Form submitted with values:", values);
      await createItem(values);
      message.success("Item created successfully");
      setIsModalOpen(false);
      searchForm.resetFields();
      fetchItems();
    } catch (error) {
      message.error("Failed to create item");
      console.error("Creation error:", error);
    }
  };

  const handleEditSubmit = async (values: EditFormValues) => {
    if (!editingItem) return;
    try {
      console.log("Updating price with:", values);
      const success = await updateItemPrice(editingItem.id, values.price);

      if (success) {
        message.success("Price updated successfully");
        setIsModalOpen(false);
        searchForm.resetFields();
        await fetchItems();
      } else {
        message.error("Price update failed");
      }
    } catch (error) {
      console.error("Update error:", error);
      message.error("Failed to update price. Please try again.");
    }
  };
  const handleEdit = (item: Item) => {
    setEditingItem(item);
    setIsModalOpen(true);
  };

  return (
    <div style={{ padding: "24px" }}>
      <InventoryStats stats={stats} />

      <Button
        type="primary"
        icon={<PlusOutlined />}
        onClick={() => {
          setEditingItem(null);
          setIsModalOpen(true);
        }}
        style={{ marginBottom: "16px" }}
      >
        Add Item
      </Button>

      <InventorySearch
        form={searchForm}
        onSearch={handleSearch}
        categories={categories}
        loading={loading}
      />

      <InventoryTable items={items} loading={loading} onEdit={handleEdit} />

      <Modal
        title={editingItem ? "Edit Item Price" : "Add New Item"}
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        destroyOnClose
      >
        {editingItem ? (
          <EditForm item={editingItem} onSubmit={handleEditSubmit} />
        ) : (
          <CreateForm onSubmit={handleCreateItem} />
        )}
        <Space style={{ marginTop: 16 }}>
          <Button
            type="primary"
            htmlType="submit"
            form={editingItem ? "edit-form" : "create-form"}
          >
            {editingItem ? "Update Price" : "Create"}
          </Button>
          <Button onClick={() => setIsModalOpen(false)}>Cancel</Button>
        </Space>
      </Modal>
    </div>
  );
};

export default App;
