import React from 'react';
import { Card, Row, Col, Timeline, Button, Avatar, Space } from 'antd';
import {
  TeamOutlined,
  RocketOutlined,
  HeartOutlined,
  SafetyOutlined,
  UserOutlined
} from '@ant-design/icons';

const About: React.FC = () => {
  const team = [
    {
      name: 'Иван Родионов',
      role: 'Основатель & CTO',
      bio: 'Генеалог с 10+ годами опыта в цифровых архивах',
      icon: '👨‍💼'
    },
    {
      name: 'Екатерина Смирнова',
      role: 'Product Manager',
      bio: 'Специалист по UX/UI и user research',
      icon: '👩‍💼'
    },
    {
      name: 'Дмитрий Иванов',
      role: 'Lead Backend Developer',
      bio: 'Эксперт в графовых БД и AI matching',
      icon: '👨‍💻'
    }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa' }}>
      {/* Hero Section */}
      <section style={{
        background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
        color: 'white',
        padding: '80px 20px',
        textAlign: 'center'
      }}>
        <h1 style={{ fontSize: '42px', marginBottom: '16px' }}>
          🌳 О проекте "Семейные корни"
        </h1>
        <p style={{ fontSize: '18px', marginBottom: '24px', opacity: 0.95 }}>
          Современная платформа для исследования генеалогии с использованием AI и графовых БД
        </p>
      </section>

      {/* Mission Section */}
      <section style={{ padding: '80px 20px', maxWidth: '1200px', margin: '0 auto' }}>
        <Row gutter={[48, 48]}>
          <Col xs={24} md={12}>
            <h2 style={{ fontSize: '32px', marginBottom: '24px' }}>
              💡 Наша миссия
            </h2>
            <p style={{ fontSize: '16px', lineHeight: '1.8', marginBottom: '16px', color: '#666' }}>
              Сделать генеалогические исследования доступными и увлекательными для каждого.
              Мы верим, что знание о своих корнях - это право каждого человека.
            </p>
            <p style={{ fontSize: '16px', lineHeight: '1.8', marginBottom: '16px', color: '#666' }}>
              Наша платформа объединяет исторические архивы, современные технологии AI
              и интуитивный интерфейс, чтобы помочь вам открыть историю вашей семьи.
            </p>
            <p style={{ fontSize: '16px', lineHeight: '1.8', color: '#666' }}>
              С "Семейными корнями" вы можете найти дальних родственников, понять миграцию
              вашей семьи и сохранить наследие для будущих поколений.
            </p>
          </Col>
          <Col xs={24} md={12}>
            <div style={{
              background: 'white',
              padding: '40px',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ marginBottom: '24px' }}>📊 Наши достижения</h3>
              <div style={{ marginBottom: '24px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#1890ff' }}>1.5М+</div>
                <div style={{ color: '#666' }}>Генеалогических записей</div>
              </div>
              <div style={{ marginBottom: '24px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#52c41a' }}>3М+</div>
                <div style={{ color: '#666' }}>Семейных связей найдено</div>
              </div>
              <div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#faad14' }}>12K+</div>
                <div style={{ color: '#666' }}>Активных пользователей</div>
              </div>
            </div>
          </Col>
        </Row>
      </section>

      {/* Values Section */}
      <section style={{ padding: '80px 20px', maxWidth: '1200px', margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: '32px', marginBottom: '48px' }}>
          🎯 Наши ценности
        </h2>
        <Row gutter={[24, 24]}>
          <Col xs={24} sm={12} lg={6}>
            <Card hoverable style={{ height: '100%', textAlign: 'center' }}>
              <HeartOutlined style={{ fontSize: '48px', color: '#eb2f96', marginBottom: '16px' }} />
              <h4>Уважение к истории</h4>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Мы относимся к вашим семейным историям с трепетом и уважением
              </p>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card hoverable style={{ height: '100%', textAlign: 'center' }}>
              <SafetyOutlined style={{ fontSize: '48px', color: '#52c41a', marginBottom: '16px' }} />
              <h4>Безопасность данных</h4>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Ваши данные защищены по стандартам ФЗ-152 с шифрованием
              </p>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card hoverable style={{ height: '100%', textAlign: 'center' }}>
              <RocketOutlined style={{ fontSize: '48px', color: '#1890ff', marginBottom: '16px' }} />
              <h4>Инновации</h4>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Используем AI и графовые БД для лучших результатов
              </p>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card hoverable style={{ height: '100%', textAlign: 'center' }}>
              <TeamOutlined style={{ fontSize: '48px', color: '#faad14', marginBottom: '16px' }} />
              <h4>Сообщество</h4>
              <p style={{ color: '#666', fontSize: '14px' }}>
                Вместе мы сильнее в исследовании истории семей
              </p>
            </Card>
          </Col>
        </Row>
      </section>

      {/* History Section */}
      <section style={{ padding: '80px 20px', maxWidth: '1000px', margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: '32px', marginBottom: '48px' }}>
          📖 История нашего развития
        </h2>
        <Timeline
          items={[
            {
              children: (
                <div>
                  <h4>2022 - Идея</h4>
                  <p style={{ color: '#666' }}>
                    Иван Родионов заметил, что генеалогические исследования требуют много времени.
                    Он решил создать платформу, которая сделает это быстрее и проще.
                  </p>
                </div>
              )
            },
            {
              children: (
                <div>
                  <h4>2023 - MVP</h4>
                  <p style={{ color: '#666' }}>
                    Запущена первая версия с поддержкой импорта GEDCOM
                    и базовым поиском совпадений.
                  </p>
                </div>
              )
            },
            {
              children: (
                <div>
                  <h4>2024 - Масштабирование</h4>
                  <p style={{ color: '#666' }}>
                    Добавлены AI-powered fuzzy matching, CRM система, аналитика.
                    Достигли 10K+ пользователей.
                  </p>
                </div>
              )
            },
            {
              children: (
                <div>
                  <h4>2025 - Глобальное расширение</h4>
                  <p style={{ color: '#666' }}>
                    Добавлена поддержка 15+ языков, интеграция с архивами EU и USA,
                    система достижений и лидербордов.
                  </p>
                </div>
              )
            }
          ]}
        />
      </section>

      {/* Team Section */}
      <section style={{ padding: '80px 20px', maxWidth: '1200px', margin: '0 auto' }}>
        <h2 style={{ textAlign: 'center', fontSize: '32px', marginBottom: '48px' }}>
          👥 Наша команда
        </h2>
        <Row gutter={[24, 24]}>
          {team.map((member, idx) => (
            <Col key={idx} xs={24} md={8}>
              <Card hoverable style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '64px', marginBottom: '16px' }}>
                  {member.icon}
                </div>
                <h3 style={{ marginBottom: '8px' }}>{member.name}</h3>
                <p style={{ color: '#1890ff', fontWeight: 'bold', marginBottom: '12px' }}>
                  {member.role}
                </p>
                <p style={{ color: '#666', fontSize: '14px' }}>
                  {member.bio}
                </p>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      {/* CTA Section */}
      <section style={{
        background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
        color: 'white',
        padding: '60px 20px',
        textAlign: 'center',
        borderRadius: '8px',
        maxWidth: '800px',
        margin: '80px auto 0'
      }}>
        <h2 style={{ marginBottom: '16px' }}>🚀 Присоединяйтесь к нам</h2>
        <p style={{ marginBottom: '24px', fontSize: '16px' }}>
          Начните исследовать историю вашей семьи прямо сейчас!
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
          Создать бесплатный аккаунт
        </Button>
      </section>
    </div>
  );
};

export default About;
