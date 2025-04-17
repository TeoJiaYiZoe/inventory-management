import React from "react";
import { Form, Input, InputNumber } from "antd";
import { Item, EditFormValues } from "../../../types";

interface Props {
  item: Item;
  onSubmit: (values: EditFormValues) => void;
}

export const EditForm: React.FC<Props> = ({ item, onSubmit }) => (
  <Form<EditFormValues>
    id="edit-form"
    onFinish={onSubmit}
    layout="vertical"
    initialValues={{ price: item.price }}
  >
    <Form.Item label="Name">
      <Input
        value={item.name}
        readOnly
        disabled
        style={{ background: "#f5f5f5", color: "rgba(0, 0, 0, 0.65)" }}
      />
    </Form.Item>
    <Form.Item label="Category">
      <Input
        value={item.category}
        readOnly
        disabled
        style={{ background: "#f5f5f5", color: "rgba(0, 0, 0, 0.65)" }}
      />
    </Form.Item>
    <Form.Item
      label="Price (SGD)"
      name="price"
      rules={[
        { required: true, message: "Please enter price" },
        { type: "number", min: 0.01, message: "Minimum price is SGD 0.01" },
      ]}
    >
      <InputNumber
        min={0.01}
        step={0.01}
        precision={2}
        style={{ width: "100%" }}
        formatter={(value) => `SGD ${value}`}
        parser={(value?: string) =>
          parseFloat(value?.replace(/[^\d.-]/g, "") || "0.01")
        }
      />
    </Form.Item>
  </Form>
);
