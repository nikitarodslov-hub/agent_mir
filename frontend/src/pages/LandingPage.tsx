import React from 'react';
import { Button, Row, Col, Card, Timeline, Testimonial, Space, Statistic } from 'antd';
import {
  CheckCircleOutlined,
  RocketOutlined,
  HeartOutlined,
  TeamOutlined,
  SafetyOutlined,
  BgColorsOutlined
} from '@ant-design/icons';

const LandingPage: React.FC = () => {
  return (
    <div style={{ background: '#f5f7fa', minHeight: '100vh' }}>
      {/* Hero Section */}
      <section style={{
        background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
        color: 'white',
        padding: '80px 20px',
        textAlign: 'center'
      }}>
        <h1 style={{ fontSize: '48px', marginBottom: '16px', fontWeight: 'bold' }}>
          🌳 Семейные корни
        </h1>
        <p style={{ fontSize: '24px', marginBottom: '32px', opacity: 0.95 }}>
          Откройте историю вашей семьи. Сохраните наследие поколений.
        </p>
        <Space size="large">
          <Button
            type="primary"
            size="large"
            style={{ height: '48px', fontSize: '16px', background: 'white', color: '#1890ff' }}
            href="/register"
          >
            Начать бесплатно
          </Button>
          <Button
            size="large"
            style={{
              height: '48px',
              fontSize: '16px',
              background: 'transparent',
              color: 'white',
              border: '2px solid white'
            }}
            href="/pricing"
          >
            Смотреть цены
          </Button>
        </Space>

        <div style={{
          marginTop: '48px',
          display: 'flex',
          justifyContent: 'center',
          gap: '48px',
          flexWrap: 'wrap'
        }}>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>1.5M+</div>
            <div>генеалогических записей</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>3M+</div>
            <div>семейных связей</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>12K+</div>
            <div>активных пользователей</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '80px 20px', maxWidth: '1200px', margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: '36px', marginBottom: '48px' }}>
          ✨ Почему выбирают нас?
        </h2>

        <Row gutter={[24, 24]}>
          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <RocketOutlined style={{ fontSize: '48px', color: '#1890ff', marginBottom: '16px' }} />
                <h3>Быстрый поиск</h3>
                <p>Найдите совпадения за секунды благодаря AI технологиям</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <SafetyOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
                <h3>Безопасность</h3>
                <p>Ваши данные защищены по стандарту ФЗ-152</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <HeartOutlined style={{ fontSize: '48px', color: '#eb2f96', marginBottom: '16px' }} />
                <h3>Сохранение наследия</h3>
                <p>Передавайте историю семьи следующему поколению</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <TeamOutlined style={{ fontSize: '48px', color: '#faad14', marginBottom: '16px' }} />
                <h3>Совместная работа</h3>
                <p>Приглашайте близких и работайте над деревом вместе</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <BgColorsOutlined style={{ fontSize: '48px', color: '#722ed1', marginBottom: '16px' }} />
                <h3>Геймификация</h3>
                <p>Получайте достижения и бонусы за активность</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card hoverable style={{ height: '100%' }}>
              <div style={{ textAlign: 'center' }}>
                <CheckCircleOutlined style={{ fontSize: '48px', color: '#13c2c2', marginBottom: '16px' }} />
                <h3>Импорт/Экспорт</h3>
                <p>Совместимо с GEDCOM, CSV и другими форматами</p>
              </div>
            </Card>
          </Col>
        </Row>
      </section>

      {/* How It Works */}
      <section style={{
        padding: '80px 20px',
        maxWidth: '1200px',
        margin: '0 auto',
        background: 'white'
      }}>
        <h2 style={{ textAlign: 'center', fontSize: '36px', marginBottom: '48px' }}>
          🎯 Как это работает?
        </h2>

        <Row gutter={[32, 32]} style={{ marginBottom: '32px' }}>
          <Col xs={24} lg={12}>
            <Timeline
              items={[
                {
                  children: <div>
                    <h3>Шаг 1: Регистрация</h3>
                    <p>Создайте бесплатный аккаунт за 2 минуты</p>
                  </div>
                },
                {
                  children: <div>
                    <h3>Шаг 2: Добавьте людей</h3>
                    <p>Начните с себя и добавьте членов семьи</p>
                  </div>
                },
                {
                  children: <div>
                    <h3>Шаг 3: Найдите связи</h3>
                    <p>Наша AI найдет совпадения и дубликаты</p>
                  </div>
                },
                {
                  children: <div>
                    <h3>Шаг 4: Постройте дерево</h3>
                    <p>Визуализируйте всю историю вашей семьи</p>
                  </div>
                }
              ]}
            />
          </Col>

          <Col xs={24} lg={12}>
            <Card style={{ background: '#f5f7fa', border: 'none' }}>
              <h3>📊 Примеры того, что вы можете делать:</h3>
              <ul style={{ lineHeight: '2' }}>
                <li>✅ Построить дерево в 1000+ поколений</li>
                <li>✅ Найти дальних родственников</li>
                <li>✅ Изучить историю миграции семьи</li>
                <li>✅ Сохранить семейные фотографии</li>
                <li>✅ Документировать семейные легенды</li>
                <li>✅ Поделиться с родственниками</li>
              </ul>
            </Card>
          </Col>
        </Row>
      </section>

      {/* Testimonials */}
      <section style={{
        padding: '80px 20px',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <h2 style={{ textAlign: 'center', fontSize: '36px', marginBottom: '48px' }}>
          💬 Отзывы пользователей
        </h2>

        <Row gutter={[24, 24]}>
          {[
            {
              name: 'Мария Петрова',
              role: 'Исследователь генеалогии',
              text: 'Отличный инструмент! За неделю нашла 200+ родственников.'
            },
            {
              name: 'Иван Сидоров',
              role: 'Учитель истории',
              text: 'Использую с студентами. Очень помогает в изучении истории семей.'
            },
            {
              name: 'Елена Смирнова',
              role: 'Пенсионерка',
              text: 'Даже я, которая не очень умею с компьютером, разобралась легко!'
            }
          ].map((testimonial, index) => (
            <Col key={index} xs={24} md={8}>
              <Card style={{ height: '100%' }}>
                <div style={{ marginBottom: '16px' }}>
                  {'⭐'.repeat(5)}
                </div>
                <p style={{ marginBottom: '16px', fontStyle: 'italic' }}>
                  "{testimonial.text}"
                </p>
                <strong>{testimonial.name}</strong>
                <div style={{ color: '#666', fontSize: '14px' }}>
                  {testimonial.role}
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      {/* CTA Section */}
      <section style={{
        background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
        color: 'white',
        padding: '80px 20px',
        textAlign: 'center'
      }}>
        <h2 style={{ fontSize: '36px', marginBottom: '32px' }}>
          🚀 Готовы начать?
        </h2>
        <p style={{ fontSize: '18px', marginBottom: '32px' }}>
          Создайте свое генеалогическое дерево прямо сейчас. Первые 50 персон — бесплатно!
        </p>
        <Button
          type="primary"
          size="large"
          style={{
            height: '48px',
            fontSize: '16px',
            background: 'white',
            color: '#1890ff'
          }}
          href="/register"
        >
          Начать бесплатно
        </Button>
      </section>

      {/* Footer */}
      <footer style={{
        background: '#1f1f1f',
        color: 'white',
        padding: '40px 20px',
        textAlign: 'center'
      }}>
        <Row gutter={[32, 32]}>
          <Col xs={24} sm={8}>
            <h4>🌳 Семейные корни</h4>
            <p>Платформа для генеалогических исследований</p>
          </Col>
          <Col xs={24} sm={8}>
            <h4>Информация</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><a href="/about" style={{ color: 'white' }}>О нас</a></li>
              <li><a href="/blog" style={{ color: 'white' }}>Блог</a></li>
              <li><a href="/faq" style={{ color: 'white' }}>Часто вопросы</a></li>
            </ul>
          </Col>
          <Col xs={24} sm={8}>
            <h4>Легально</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><a href="/terms" style={{ color: 'white' }}>Условия</a></li>
              <li><a href="/privacy" style={{ color: 'white' }}>Приватность</a></li>
              <li><a href="/contact" style={{ color: 'white' }}>Контакты</a></li>
            </ul>
          </Col>
        </Row>
        <hr style={{ margin: '32px 0', opacity: 0.2 }} />
        <p>&copy; 2024 Семейные корни. Все права защищены.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
