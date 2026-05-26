import React from 'react';
import { Row, Col, Divider } from 'antd';
import { GithubOutlined, LinkedinOutlined, MailOutlined } from '@ant-design/icons';

const Footer: React.FC = () => {
  return (
    <footer style={{
      background: '#1f1f1f',
      color: 'white',
      padding: '60px 20px 20px',
      marginTop: '80px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Row gutter={[32, 32]} style={{ marginBottom: '40px' }}>
          <Col xs={24} sm={12} md={6}>
            <h4 style={{ marginBottom: '16px' }}>🌳 Семейные корни</h4>
            <p style={{ color: '#ccc', fontSize: '14px' }}>
              Платформа для генеалогических исследований с использованием AI и графовых БД.
            </p>
          </Col>

          <Col xs={24} sm={12} md={6}>
            <h4 style={{ marginBottom: '16px' }}>Информация</h4>
            <ul style={{ listStyle: 'none', padding: 0, color: '#ccc' }}>
              <li style={{ marginBottom: '8px' }}>
                <a href="/about" style={{ color: '#ccc', textDecoration: 'none' }}>О нас</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="/pricing" style={{ color: '#ccc', textDecoration: 'none' }}>Цены</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="/faq" style={{ color: '#ccc', textDecoration: 'none' }}>Часто вопросы</a>
              </li>
              <li>
                <a href="/blog" style={{ color: '#ccc', textDecoration: 'none' }}>Блог</a>
              </li>
            </ul>
          </Col>

          <Col xs={24} sm={12} md={6}>
            <h4 style={{ marginBottom: '16px' }}>Поддержка</h4>
            <ul style={{ listStyle: 'none', padding: 0, color: '#ccc' }}>
              <li style={{ marginBottom: '8px' }}>
                <a href="/contact" style={{ color: '#ccc', textDecoration: 'none' }}>Контакты</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="mailto:support@familyroots.ru" style={{ color: '#ccc', textDecoration: 'none' }}>Email поддержка</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="https://t.me/familyroots_support" style={{ color: '#ccc', textDecoration: 'none' }}>Telegram</a>
              </li>
              <li>
                <a href="/terms" style={{ color: '#ccc', textDecoration: 'none' }}>Обратная связь</a>
              </li>
            </ul>
          </Col>

          <Col xs={24} sm={12} md={6}>
            <h4 style={{ marginBottom: '16px' }}>Легально</h4>
            <ul style={{ listStyle: 'none', padding: 0, color: '#ccc' }}>
              <li style={{ marginBottom: '8px' }}>
                <a href="/terms" style={{ color: '#ccc', textDecoration: 'none' }}>Условия</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="/privacy" style={{ color: '#ccc', textDecoration: 'none' }}>Приватность</a>
              </li>
              <li style={{ marginBottom: '8px' }}>
                <a href="/terms" style={{ color: '#ccc', textDecoration: 'none' }}>Cookies</a>
              </li>
              <li>
                <a href="/terms" style={{ color: '#ccc', textDecoration: 'none' }}>GDPR</a>
              </li>
            </ul>
          </Col>
        </Row>

        <Divider style={{ borderColor: '#444', margin: '20px 0' }} />

        <Row gutter={[16, 16]} style={{ marginBottom: '24px', alignItems: 'center' }}>
          <Col xs={24} md={12}>
            <p style={{ color: '#ccc', marginBottom: '0' }}>
              &copy; 2024 Семейные корни. Все права защищены.
            </p>
          </Col>
          <Col xs={24} md={12} style={{ textAlign: 'right' }}>
            <div style={{ display: 'flex', gap: '16px', justifyContent: 'flex-end' }}>
              <a href="https://github.com/nikitarodslov-hub/agent_mir" style={{ color: '#ccc' }}>
                <GithubOutlined style={{ fontSize: '20px' }} />
              </a>
              <a href="https://linkedin.com" style={{ color: '#ccc' }}>
                <LinkedinOutlined style={{ fontSize: '20px' }} />
              </a>
              <a href="mailto:support@familyroots.ru" style={{ color: '#ccc' }}>
                <MailOutlined style={{ fontSize: '20px' }} />
              </a>
            </div>
          </Col>
        </Row>

        <p style={{ color: '#999', fontSize: '12px', textAlign: 'center', marginBottom: '0' }}>
          Платформа разработана для исследования генеалогии с соблюдением стандартов защиты данных
        </p>
      </div>
    </footer>
  );
};

export default Footer;
