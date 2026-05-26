import React, { useState } from 'react';
import { Card, Row, Col, Form, Input, Button, Select, Avatar, Space, Divider, Switch } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons';

const Profile: React.FC = () => {
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();

  const handleSave = () => {
    form.validateFields().then((values) => {
      console.log('Сохранить профиль:', values);
      setEditing(false);
    });
  };

  return (
    <div>
      <h1>👤 Мой профиль</h1>

      <Row gutter={16}>
        <Col xs={24} sm={12} md={6}>
          <Card style={{ textAlign: 'center' }}>
            <Avatar size={120} icon={<UserOutlined />} style={{ background: '#1890ff' }} />
            <h2 style={{ marginTop: '16px' }}>Иван Петров</h2>
            <p style={{ color: '#666' }}>Уровень 7</p>
            <p style={{ color: '#999' }}>2,850 очков</p>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={18}>
          <Card title="Основная информация">
            <Form
              form={form}
              layout="vertical"
              disabled={!editing}
              initialValues={{
                fullName: 'Иван Петрович Петров',
                email: 'ivan@example.com',
                phone: '+7 (999) 123-45-67',
                birthdate: '1980-01-15',
                birthplace: 'Уфа, Республика Башкортостан',
                subscription: 'researcher'
              }}
            >
              <Row gutter={16}>
                <Col xs={24} sm={12}>
                  <Form.Item label="Полное имя" name="fullName">
                    <Input placeholder="Иван Петров" />
                  </Form.Item>
                </Col>
                <Col xs={24} sm={12}>
                  <Form.Item label="Email" name="email">
                    <Input type="email" icon={<MailOutlined />} />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col xs={24} sm={12}>
                  <Form.Item label="Телефон" name="phone">
                    <Input icon={<PhoneOutlined />} />
                  </Form.Item>
                </Col>
                <Col xs={24} sm={12}>
                  <Form.Item label="Дата рождения" name="birthdate">
                    <Input type="date" />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item label="Место рождения" name="birthplace">
                <Input placeholder="Город, область" />
              </Form.Item>

              <Row gutter={16}>
                <Col xs={24}>
                  <Space>
                    {editing ? (
                      <>
                        <Button type="primary" onClick={handleSave}>
                          Сохранить
                        </Button>
                        <Button onClick={() => setEditing(false)}>
                          Отмена
                        </Button>
                      </>
                    ) : (
                      <Button onClick={() => setEditing(true)}>
                        Редактировать
                      </Button>
                    )}
                  </Space>
                </Col>
              </Row>
            </Form>
          </Card>
        </Col>
      </Row>

      <Card title="💳 Подписка" style={{ marginTop: '16px' }}>
        <Row gutter={16}>
          <Col xs={24} sm={12}>
            <Form layout="vertical" initialValues={{ subscription: 'researcher' }}>
              <Form.Item label="Текущий тариф" name="subscription">
                <Select disabled>
                  <Select.Option value="free">Бесплатный</Select.Option>
                  <Select.Option value="researcher">Исследователь (2,490 ₽/год)</Select.Option>
                  <Select.Option value="professional">Профессионал (30,000 ₽/год)</Select.Option>
                </Select>
              </Form.Item>
            </Form>
          </Col>
          <Col xs={24} sm={12}>
            <Form layout="vertical">
              <Form.Item label="Действительна до">
                <Input value="2024-12-31" disabled />
              </Form.Item>
            </Form>
          </Col>
        </Row>

        <Divider />

        <h3>Доступные функции:</h3>
        <ul>
          <li>✓ Неограниченное количество персон</li>
          <li>✓ Интеллектуальный поиск совпадений</li>
          <li>✓ Защищенное хранилище</li>
          <li>✓ Экспорт в GEDCOM</li>
          <li>✗ Профессиональная лицензия</li>
        </ul>

        <Button type="primary" size="large" style={{ marginTop: '16px' }}>
          Обновить подписку
        </Button>
      </Card>

      <Card title="⚙️ Настройки приватности" style={{ marginTop: '16px' }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Открытый профиль</span>
            <Switch />
          </div>

          <Divider style={{ margin: '12px 0' }} />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Показывать достижения</span>
            <Switch defaultChecked />
          </div>

          <Divider style={{ margin: '12px 0' }} />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Разрешить поиск по имени</span>
            <Switch defaultChecked />
          </div>

          <Divider style={{ margin: '12px 0' }} />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Получать уведомления</span>
            <Switch defaultChecked />
          </div>
        </Space>
      </Card>

      <Card title="🔐 Безопасность" style={{ marginTop: '16px' }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Button block>Изменить пароль</Button>
          <Button block danger>Отвязать аккаунт VK</Button>
          <Button block danger>Выход со всех устройств</Button>
          <Divider />
          <Button block danger type="text">Удалить аккаунт</Button>
        </Space>
      </Card>
    </div>
  );
};

export default Profile;
