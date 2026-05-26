import React, { useState } from 'react';
import { Card, Row, Col, Form, Input, Button, Tabs, Tag, Modal, message, Avatar, Divider, Space } from 'antd';
import { EditOutlined, DeleteOutlined, LockOutlined, LogoutOutlined, CreditCardOutlined } from '@ant-design/icons';

const Account: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);

  // Mock user data
  const user = {
    name: 'Иван Петров',
    email: 'ivan@example.com',
    joinDate: '2024-01-15',
    subscription: 'Researcher',
    subscriptionEnd: '2025-01-15',
    status: 'active'
  };

  const onSaveProfile = async (values: any) => {
    setLoading(true);
    try {
      console.log('Saving profile:', values);
      message.success('Профиль обновлен успешно!');
    } catch (error) {
      message.error('Ошибка при сохранении профиля');
    } finally {
      setLoading(false);
    }
  };

  const onChangePassword = async (values: any) => {
    setLoading(true);
    try {
      console.log('Changing password');
      message.success('Пароль изменен успешно!');
    } catch (error) {
      message.error('Ошибка при изменении пароля');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa', padding: '40px 20px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '32px', marginBottom: '32px' }}>
          👤 Мой аккаунт
        </h1>

        <Tabs
          defaultActiveKey="1"
          items={[
            {
              key: '1',
              label: '📋 Профиль',
              children: (
                <Row gutter={[24, 24]}>
                  <Col xs={24} lg={12}>
                    <Card title="Основная информация">
                      <div style={{ marginBottom: '24px', textAlign: 'center' }}>
                        <Avatar size={120} icon="👤" style={{ marginBottom: '16px' }} />
                        <div>
                          <h3 style={{ marginBottom: '4px' }}>{user.name}</h3>
                          <p style={{ color: '#666', marginBottom: '0' }}>{user.email}</p>
                        </div>
                      </div>

                      <Form
                        form={form}
                        layout="vertical"
                        onFinish={onSaveProfile}
                        initialValues={{
                          name: user.name,
                          email: user.email
                        }}
                      >
                        <Form.Item
                          label="Имя"
                          name="name"
                          rules={[{ required: true, message: 'Введите имя' }]}
                        >
                          <Input />
                        </Form.Item>

                        <Form.Item
                          label="Email"
                          name="email"
                          rules={[{ required: true, type: 'email', message: 'Некорректный email' }]}
                        >
                          <Input />
                        </Form.Item>

                        <Form.Item
                          label="Телефон (опционально)"
                          name="phone"
                        >
                          <Input />
                        </Form.Item>

                        <Form.Item
                          label="Биография (опционально)"
                          name="bio"
                        >
                          <Input.TextArea rows={3} />
                        </Form.Item>

                        <Button type="primary" htmlType="submit" block loading={loading}>
                          <EditOutlined /> Сохранить изменения
                        </Button>
                      </Form>
                    </Card>
                  </Col>

                  <Col xs={24} lg={12}>
                    <Card title="📊 Информация об аккаунте">
                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Дата присоединения
                        </div>
                        <div style={{ fontSize: '16px', fontWeight: 'bold' }}>
                          15 января 2024
                        </div>
                      </div>

                      <Divider />

                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Всего персон в дереве
                        </div>
                        <div style={{ fontSize: '16px', fontWeight: 'bold' }}>
                          1,234
                        </div>
                      </div>

                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Найдено совпадений
                        </div>
                        <div style={{ fontSize: '16px', fontWeight: 'bold' }}>
                          89
                        </div>
                      </div>

                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Достижений разблокировано
                        </div>
                        <div style={{ fontSize: '16px', fontWeight: 'bold' }}>
                          23
                        </div>
                      </div>

                      <Divider />

                      <Button type="dashed" block danger onClick={() => setDeleteModalOpen(true)}>
                        <DeleteOutlined /> Удалить аккаунт
                      </Button>
                    </Card>
                  </Col>
                </Row>
              )
            },
            {
              key: '2',
              label: '💳 Подписка',
              children: (
                <Row gutter={[24, 24]}>
                  <Col xs={24} lg={12}>
                    <Card title="Текущая подписка">
                      <div style={{ marginBottom: '16px', textAlign: 'center' }}>
                        <Tag color="green" style={{ padding: '8px 16px', fontSize: '14px' }}>
                          Активна
                        </Tag>
                      </div>

                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          План
                        </div>
                        <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                          Researcher
                        </div>
                      </div>

                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Цена
                        </div>
                        <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                          2,490 ₽/год
                        </div>
                      </div>

                      <div style={{ marginBottom: '24px' }}>
                        <div style={{ color: '#666', fontSize: '12px', marginBottom: '4px' }}>
                          Возобновление
                        </div>
                        <div style={{ fontSize: '16px' }}>
                          15 января 2025
                        </div>
                      </div>

                      <Space direction="vertical" style={{ width: '100%' }}>
                        <Button type="primary" block>
                          <CreditCardOutlined /> Обновить платежные данные
                        </Button>
                        <Button danger block>
                          Отменить подписку
                        </Button>
                      </Space>
                    </Card>
                  </Col>

                  <Col xs={24} lg={12}>
                    <Card title="Доступные функции">
                      <div>
                        <div style={{ marginBottom: '12px' }}>
                          <span style={{ color: '#52c41a', fontWeight: 'bold' }}>✅</span> Неограниченные персоны
                        </div>
                        <div style={{ marginBottom: '12px' }}>
                          <span style={{ color: '#52c41a', fontWeight: 'bold' }}>✅</span> Полный Fuzzy Matching
                        </div>
                        <div style={{ marginBottom: '12px' }}>
                          <span style={{ color: '#52c41a', fontWeight: 'bold' }}>✅</span> Защищенное хранилище (1 ГБ)
                        </div>
                        <div style={{ marginBottom: '12px' }}>
                          <span style={{ color: '#52c41a', fontWeight: 'bold' }}>✅</span> Импорт/Экспорт GEDCOM
                        </div>
                        <div style={{ marginBottom: '12px' }}>
                          <span style={{ color: '#52c41a', fontWeight: 'bold' }}>✅</span> Приватное дерево
                        </div>
                        <div>
                          <span style={{ color: '#d9d9d9', fontWeight: 'bold' }}>❌</span> CRM система (только Pro)
                        </div>
                        <div>
                          <span style={{ color: '#d9d9d9', fontWeight: 'bold' }}>❌</span> Аналитика (только Pro)
                        </div>
                      </div>
                    </Card>
                  </Col>

                  <Col xs={24}>
                    <Card title="История платежей">
                      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                          <tr style={{ borderBottom: '1px solid #ddd' }}>
                            <th style={{ padding: '12px', textAlign: 'left' }}>Дата</th>
                            <th style={{ padding: '12px', textAlign: 'left' }}>Описание</th>
                            <th style={{ padding: '12px', textAlign: 'right' }}>Сумма</th>
                            <th style={{ padding: '12px', textAlign: 'center' }}>Статус</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr style={{ borderBottom: '1px solid #eee' }}>
                            <td style={{ padding: '12px' }}>15.01.2024</td>
                            <td style={{ padding: '12px' }}>Подписка Researcher (годовая)</td>
                            <td style={{ padding: '12px', textAlign: 'right' }}>2,490 ₽</td>
                            <td style={{ padding: '12px', textAlign: 'center' }}>
                              <Tag color="green">Успешно</Tag>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </Card>
                  </Col>
                </Row>
              )
            },
            {
              key: '3',
              label: '🔐 Безопасность',
              children: (
                <Row gutter={[24, 24]}>
                  <Col xs={24} lg={12}>
                    <Card title="Изменить пароль">
                      <Form layout="vertical" onFinish={onChangePassword}>
                        <Form.Item
                          label="Текущий пароль"
                          name="currentPassword"
                          rules={[{ required: true, message: 'Введите текущий пароль' }]}
                        >
                          <Input.Password />
                        </Form.Item>

                        <Form.Item
                          label="Новый пароль"
                          name="newPassword"
                          rules={[
                            { required: true, message: 'Введите новый пароль' },
                            { min: 8, message: 'Пароль должен быть не менее 8 символов' }
                          ]}
                        >
                          <Input.Password />
                        </Form.Item>

                        <Form.Item
                          label="Подтвердите пароль"
                          name="confirmPassword"
                          dependencies={['newPassword']}
                          rules={[
                            { required: true, message: 'Подтвердите пароль' },
                            ({ getFieldValue }) => ({
                              validator(_, value) {
                                if (!value || getFieldValue('newPassword') === value) {
                                  return Promise.resolve();
                                }
                                return Promise.reject(new Error('Пароли не совпадают'));
                              }
                            })
                          ]}
                        >
                          <Input.Password />
                        </Form.Item>

                        <Button type="primary" htmlType="submit" block loading={loading}>
                          <LockOutlined /> Изменить пароль
                        </Button>
                      </Form>
                    </Card>
                  </Col>

                  <Col xs={24} lg={12}>
                    <Card title="Двухфакторная аутентификация">
                      <div style={{ marginBottom: '16px' }}>
                        <div style={{ marginBottom: '8px' }}>
                          <span style={{ fontWeight: 'bold' }}>Статус:</span> Отключена
                        </div>
                        <p style={{ color: '#666', fontSize: '14px' }}>
                          Двухфакторная аутентификация добавляет дополнительный уровень защиты к вашему аккаунту.
                          После включения вам потребуется ввести код при входе.
                        </p>
                      </div>

                      <Button type="primary" block>
                        Включить 2FA
                      </Button>
                    </Card>

                    <Card style={{ marginTop: '24px' }} title="Активные сессии">
                      <div style={{ marginBottom: '12px' }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                          Браузер на Windows
                        </div>
                        <div style={{ fontSize: '12px', color: '#666' }}>
                          Последняя активность: сейчас
                        </div>
                      </div>

                      <Button type="dashed" danger size="small" block>
                        <LogoutOutlined /> Выход из других сессий
                      </Button>
                    </Card>
                  </Col>
                </Row>
              )
            },
            {
              key: '4',
              label: '📧 Уведомления',
              children: (
                <Card title="Предпочтения уведомлений">
                  <Form layout="vertical">
                    <Form.Item>
                      <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'flex', alignItems: 'center' }}>
                          <input type="checkbox" defaultChecked style={{ marginRight: '8px' }} />
                          <span>Уведомления о новых совпадениях</span>
                        </label>
                      </div>
                      <label style={{ display: 'flex', alignItems: 'center' }}>
                        <input type="checkbox" defaultChecked style={{ marginRight: '8px' }} />
                        <span>Еженедельные дайджесты</span>
                      </label>
                    </Form.Item>

                    <Form.Item>
                      <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'flex', alignItems: 'center' }}>
                          <input type="checkbox" defaultChecked style={{ marginRight: '8px' }} />
                          <span>Уведомления о разблокировке достижений</span>
                        </label>
                      </div>
                      <label style={{ display: 'flex', alignItems: 'center' }}>
                        <input type="checkbox" style={{ marginRight: '8px' }} />
                        <span>Маркетинговые письма и рекламные предложения</span>
                      </label>
                    </Form.Item>

                    <Button type="primary" block>
                      Сохранить предпочтения
                    </Button>
                  </Form>
                </Card>
              )
            }
          ]}
        />
      </div>

      <Modal
        title="Удалить аккаунт"
        open={deleteModalOpen}
        okText="Удалить"
        cancelText="Отмена"
        okButtonProps={{ danger: true }}
        onOk={() => {
          message.success('Ваш аккаунт будет удален в течение 30 дней');
          setDeleteModalOpen(false);
        }}
        onCancel={() => setDeleteModalOpen(false)}
      >
        <p>⚠️ Это действие необратимо!</p>
        <p>
          Если вы удалите свой аккаунт, все ваши данные будут удалены в течение 30 дней.
          Вы сможете восстановить аккаунт в течение этого периода.
        </p>
      </Modal>
    </div>
  );
};

export default Account;
