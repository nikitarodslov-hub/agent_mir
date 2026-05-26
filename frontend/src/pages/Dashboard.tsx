import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Button, Space, Progress, Empty } from 'antd';
import { UserOutlined, TeamOutlined, LinkOutlined, FireOutlined } from '@ant-design/icons';
import axios from 'axios';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/genealogy/statistics`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setStats(response.data.statistics);
    } catch (error) {
      console.error('Ошибка загрузки статистики:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>📊 Главная</h1>

      <Row gutter={16} style={{ marginBottom: '32px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Всего персон"
              value={stats?.total_persons || 0}
              icon={<UserOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Связей создано"
              value={stats?.total_relationships || 0}
              icon={<LinkOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Достижения"
              value={8}
              suffix="/ 25"
              icon={<FireOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Уровень"
              value={7}
              suffix="🎖️"
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col xs={24} lg={12}>
          <Card title="🚀 Быстрый старт" hoverable>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div>
                <h3>Добро пожаловать в Семейные корни!</h3>
                <p>Начните с добавления членов вашей семьи и создания генеалогического дерева.</p>
              </div>

              <Space direction="vertical" style={{ width: '100%' }}>
                <Button type="primary" size="large" block>
                  ➕ Добавить персону
                </Button>
                <Button size="large" block>
                  📂 Импортировать GEDCOM
                </Button>
                <Button size="large" block>
                  🔍 Начать поиск
                </Button>
              </Space>

              <div>
                <h4>💡 Совет дня:</h4>
                <p>Используйте Fuzzy Matching для поиска дубликатов в вашем дереве. Это сэкономит вам время!</p>
              </div>
            </Space>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title="🏆 Текущие достижения" hoverable>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>Архивист (45%)</strong>
                </div>
                <Progress percent={45} />
              </div>

              <div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>Летописец (60%)</strong>
                </div>
                <Progress percent={60} status="active" />
              </div>

              <div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>Сыщик (20%)</strong>
                </div>
                <Progress percent={20} status="exception" />
              </div>

              <Button type="primary" block>
                Посмотреть все достижения
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: '32px' }}>
        <Col xs={24}>
          <Card title="📚 Недавние действия">
            <Empty description="Нет действий" style={{ marginTop: '32px' }} />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
