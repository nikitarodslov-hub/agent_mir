import React, { useState } from 'react';
import { Card, Form, Input, Button, Row, Col, message, Space } from 'antd';
import { MailOutlined, PhoneOutlined, EnvironmentOutlined, LinkedinOutlined, GithubOutlined } from '@ant-design/icons';

const Contact: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      // В реальном приложении отправить на backend
      console.log('Contact form:', values);
      message.success('Спасибо! Мы получили вашу заявку и ответим в течение 24 часов.');
      form.resetFields();
    } catch (error) {
      message.error('Ошибка при отправке формы. Попробуйте позже.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa', padding: '40px 20px' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '60px' }}>
        <h1 style={{ fontSize: '42px', marginBottom: '16px' }}>
          📞 Свяжитесь с нами
        </h1>
        <p style={{ fontSize: '18px', color: '#666' }}>
          У вас есть вопросы? Мы здесь, чтобы помочь.
        </p>
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Row gutter={[32, 32]}>
          {/* Contact Form */}
          <Col xs={24} lg={12}>
            <Card style={{ height: '100%' }}>
              <h2 style={{ marginBottom: '24px' }}>✉️ Отправить сообщение</h2>
              <Form
                form={form}
                layout="vertical"
                onFinish={onFinish}
              >
                <Form.Item
                  name="name"
                  label="Ваше имя"
                  rules={[{ required: true, message: 'Пожалуйста, введите имя' }]}
                >
                  <Input placeholder="Иван Петров" size="large" />
                </Form.Item>

                <Form.Item
                  name="email"
                  label="Email"
                  rules={[
                    { required: true, message: 'Пожалуйста, введите email' },
                    { type: 'email', message: 'Некорректный email' }
                  ]}
                >
                  <Input placeholder="ivan@example.com" size="large" type="email" />
                </Form.Item>

                <Form.Item
                  name="phone"
                  label="Телефон (опционально)"
                >
                  <Input placeholder="+7 (999) 999-99-99" size="large" />
                </Form.Item>

                <Form.Item
                  name="subject"
                  label="Тема"
                  rules={[{ required: true, message: 'Пожалуйста, введите тему' }]}
                >
                  <Input placeholder="Вопрос о подписке" size="large" />
                </Form.Item>

                <Form.Item
                  name="message"
                  label="Сообщение"
                  rules={[{ required: true, message: 'Пожалуйста, введите сообщение' }]}
                >
                  <Input.TextArea
                    placeholder="Расскажите нам о вашей проблеме или вопросе..."
                    rows={6}
                  />
                </Form.Item>

                <Button
                  type="primary"
                  htmlType="submit"
                  size="large"
                  block
                  loading={loading}
                >
                  Отправить
                </Button>
              </Form>
            </Card>
          </Col>

          {/* Contact Info */}
          <Col xs={24} lg={12}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              {/* Support Card */}
              <Card>
                <h3 style={{ marginBottom: '16px' }}>🎯 Служба поддержки</h3>
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Email</div>
                    <a href="mailto:support@familyroots.ru" style={{ color: '#1890ff' }}>
                      <MailOutlined /> support@familyroots.ru
                    </a>
                  </div>
                  <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Telegram</div>
                    <a href="https://t.me/familyroots_support" style={{ color: '#1890ff' }}>
                      💬 @familyroots_support
                    </a>
                  </div>
                  <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Часы работы</div>
                    <div style={{ color: '#666' }}>Пн-Пт: 09:00 - 18:00 МСК</div>
                  </div>
                </Space>
              </Card>

              {/* Office Card */}
              <Card>
                <h3 style={{ marginBottom: '16px' }}>🏢 Офис</h3>
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div>
                    <EnvironmentOutlined /> Москва, Россия
                  </div>
                  <div style={{ color: '#666', fontSize: '14px' }}>
                    Основной офис нашей компании находится в Москве.
                    Приезжайте в гости!
                  </div>
                </Space>
              </Card>

              {/* Social Media Card */}
              <Card>
                <h3 style={{ marginBottom: '16px' }}>🔗 Следите за нами</h3>
                <Space>
                  <a href="https://github.com/nikitarodslov-hub/agent_mir" target="_blank" rel="noopener noreferrer">
                    <GithubOutlined style={{ fontSize: '24px' }} />
                  </a>
                  <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
                    <LinkedinOutlined style={{ fontSize: '24px', color: '#0077B5' }} />
                  </a>
                  <a href="https://t.me/familyroots" target="_blank" rel="noopener noreferrer">
                    <div style={{ fontSize: '24px' }}>💬</div>
                  </a>
                </Space>
              </Card>

              {/* FAQ Card */}
              <Card style={{ background: '#f5f7fa' }}>
                <h3 style={{ marginBottom: '16px' }}>❓ Быстрые ответы</h3>
                <div style={{ fontSize: '14px', color: '#666' }}>
                  <p>
                    <strong>Как долго обрабатываются заявки?</strong><br />
                    Обычно в течение 24 часов.
                  </p>
                  <p>
                    <strong>Доступна ли техническая поддержка?</strong><br />
                    Да, для всех пользователей, включая Free план.
                  </p>
                  <p>
                    <strong>Как отменить подписку?</strong><br />
                    В разделе "Мой аккаунт" → "Подписка" → "Отменить".
                  </p>
                </div>
              </Card>
            </div>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default Contact;
