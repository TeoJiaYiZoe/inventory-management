import React from "react";
import { Form, Input, InputNumber } from "antd";
import { CreateFormValues } from "../../../types";

interface Props {
  onSubmit: (values: CreateFormValues) => void;
}

export const CreateForm: React.FC<Props> = ({ onSubmit }) => (
  <Form<CreateFormValues>
    id="create-form"
    onFinish={onSubmit}
    layout="vertical"
    initialValues={{ price: 0.01 }}
  >
    <Form.Item
      label="Name"
      name="name"
      rules={[
        { required: true, message: "Please enter item name" },
        { min: 1, max: 100 },
      ]}
    >
      <Input placeholder="Enter item name" />
    </Form.Item>
    <Form.Item
      label="Category"
      name="category"
      rules={[
        { required: true, message: "Please enter category" },
        { min: 1, max: 50 },
      ]}
    >
      <Input placeholder="Enter category" />
    </Form.Item>
    <Form.Item
      label="Price (SGD)"
      name="price"
      rules={[{ required: true }, { type: "number", min: 0.01 }]}
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
