import React, { useState } from 'react';
import { Card, Input, Button, Table, Space, Tag, Empty, Spin } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import axios from 'axios';

const Search: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/search/by-name`,
        {
          params: { q: query },
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setResults(response.data.results);
    } catch (error) {
      console.error('Ошибка поиска:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Имя',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: 'Рождение',
      dataIndex: 'birth_date',
      key: 'birth_date'
    },
    {
      title: 'Место',
      dataIndex: 'birthplace',
      key: 'birthplace'
    },
    {
      title: 'Уверенность',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => {
        const color = confidence > 0.9 ? 'green' : confidence > 0.7 ? 'orange' : 'red';
        return <Tag color={color}>{Math.round(confidence * 100)}%</Tag>;
      }
    },
    {
      title: 'Действия',
      key: 'actions',
      render: () => (
        <Space>
          <Button type="link" size="small">Просмотр</Button>
          <Button type="link" size="small">Объединить</Button>
        </Space>
      )
    }
  ];

  return (
    <div>
      <h1>🔍 Поиск родственников</h1>

      <Card style={{ marginBottom: '16px' }}>
        <Space.Compact style={{ width: '100%' }}>
          <Input
            size="large"
            placeholder="Введите имя для поиска..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onPressEnter={handleSearch}
          />
          <Button
            size="large"
            type="primary"
            icon={<SearchOutlined />}
            onClick={handleSearch}
            loading={loading}
          >
            Поиск
          </Button>
        </Space.Compact>
      </Card>

      <Card>
        <Spin spinning={loading}>
          {results.length === 0 ? (
            <Empty
              description={query ? 'Результатов не найдено' : 'Введите запрос для поиска'}
              style={{ marginTop: '48px' }}
            />
          ) : (
            <Table
              columns={columns}
              dataSource={results}
              rowKey="id"
              pagination={{ pageSize: 20 }}
            />
          )}
        </Spin>
      </Card>

      <Card title="🆚 Продвинутый поиск" style={{ marginTop: '16px' }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Button type="primary" block size="large">
            Найти дубликаты
          </Button>
          <Button block size="large">
            Найти общих предков
          </Button>
          <Button block size="large">
            Глобальный поиск по архивам
          </Button>
        </Space>
      </Card>
    </div>
  );
};

export default Search;
