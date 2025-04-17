import React from "react";
import { Row, Col, Card, Statistic } from "antd";
import { Stats } from "../../types";

interface Props {
  stats: Stats;
}

export const InventoryStats: React.FC<Props> = ({ stats }) => (
  <Row gutter={16} style={{ marginBottom: "16px" }}>
    <Col span={12}>
      <Card>
        <Statistic title="Total Items" value={stats.totalItems} precision={0} />
      </Card>
    </Col>
    <Col span={12}>
      <Card>
        <Statistic
          title="Total Inventory Value"
          value={stats.totalValue}
          precision={2}
          prefix="SGD"
        />
      </Card>
    </Col>
  </Row>
);
