import React, { useEffect, useRef } from 'react';
import { Card, Button, Space, Modal, Form, Input, Select } from 'antd';
import { PlusOutlined, DownloadOutlined, UploadOutlined } from '@ant-design/icons';
import * as d3 from 'd3';

const FamilyTree: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [modalOpen, setModalOpen] = React.useState(false);

  useEffect(() => {
    drawTree();
  }, []);

  const drawTree = () => {
    if (!svgRef.current) return;

    // Очистить SVG
    d3.select(svgRef.current).selectAll("*").remove();

    const width = 1000;
    const height = 600;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .style('border', '1px solid #ddd');

    // Пример данных для дерева
    const data = {
      name: "Иван Петров",
      children: [
        {
          name: "Петр Иванович",
          children: [
            { name: "Сергей Петрович" },
            { name: "Мария Петровна" }
          ]
        },
        {
          name: "Мария Ивановна"
        }
      ]
    };

    const root = d3.hierarchy(data);
    const tree = d3.tree().size([width, height]);
    tree(root);

    // Рисуем связи
    svg.selectAll('.link')
      .data(root.links())
      .enter()
      .append('line')
      .attr('class', 'link')
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
      .style('stroke', '#999')
      .style('stroke-width', 2);

    // Рисуем узлы
    svg.selectAll('.node')
      .data(root.descendants())
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', 20)
      .style('fill', '#1890ff')
      .style('stroke', '#fff')
      .style('stroke-width', 2)
      .style('cursor', 'pointer');

    // Рисуем подписи
    svg.selectAll('.label')
      .data(root.descendants())
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', d => d.x)
      .attr('y', d => d.y + 40)
      .text(d => d.data.name)
      .style('text-anchor', 'middle')
      .style('font-size', '12px');
  };

  return (
    <div>
      <h1>🌳 Мое генеалогическое дерево</h1>

      <Card style={{ marginBottom: '16px' }}>
        <Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalOpen(true)}
          >
            Добавить персону
          </Button>
          <Button icon={<UploadOutlined />}>
            Импортировать
          </Button>
          <Button icon={<DownloadOutlined />}>
            Экспортировать
          </Button>
        </Space>
      </Card>

      <Card>
        <div style={{ overflowX: 'auto' }}>
          <svg ref={svgRef} style={{ background: '#fafafa' }} />
        </div>
      </Card>

      <Modal
        title="Добавить новую персону"
        open={modalOpen}
        onOk={() => setModalOpen(false)}
        onCancel={() => setModalOpen(false)}
      >
        <Form layout="vertical">
          <Form.Item label="Имя" required>
            <Input placeholder="Иван Петрович" />
          </Form.Item>

          <Form.Item label="Пол" required>
            <Select>
              <Select.Option value="M">Мужской</Select.Option>
              <Select.Option value="F">Женский</Select.Option>
              <Select.Option value="U">Неизвестно</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item label="Дата рождения">
            <Input type="date" />
          </Form.Item>

          <Form.Item label="Место рождения">
            <Input placeholder="Уфа, Башкортостан" />
          </Form.Item>

          <Form.Item label="Сословие">
            <Select>
              <Select.Option value="nobleman">Дворянин</Select.Option>
              <Select.Option value="merchant">Купец</Select.Option>
              <Select.Option value="peasant">Крестьянин</Select.Option>
              <Select.Option value="townspeople">Мещанин</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default FamilyTree;
