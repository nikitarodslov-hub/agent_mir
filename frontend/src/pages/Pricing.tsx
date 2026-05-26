import React, { useState } from 'react';
import { Card, Button, Row, Col, Table, Modal, Form, Input, message } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, CreditCardOutlined } from '@ant-design/icons';

const Pricing: React.FC = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [form] = Form.useForm();

  const plans = [
    {
      name: 'Free',
      price: '0',
      currency: '₽',
      period: 'Всегда',
      description: 'Идеально для начинающих',
      color: '#1890ff',
      features: [
        { name: 'Персон в дереве', free: '50', researcher: '∞', professional: '∞' },
        { name: 'Поиск совпадений', free: '❌', researcher: '✅ Полный', professional: '✅ Полный' },
        { name: 'Защищенное хранилище', free: '❌', researcher: '✅ 1 ГБ', professional: '✅ 10 ГБ' },
        { name: 'Импорт/экспорт', free: '❌', researcher: '✅', professional: '✅' },
        { name: 'Видимость дерева', free: '❌', researcher: '✅ Приватно', professional: '✅ Приватно' },
        { name: 'CRM система', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Аналитика', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Приоритетная поддержка', free: '❌', researcher: '❌', professional: '✅ 24/7' },
      ],
      cta: 'Начать бесплатно',
      ctaLink: '/register'
    },
    {
      name: 'Researcher',
      price: '2,490',
      currency: '₽',
      period: '/год',
      description: 'Для исследователей',
      color: '#52c41a',
      popular: true,
      features: [
        { name: 'Персон в дереве', free: '50', researcher: '∞', professional: '∞' },
        { name: 'Поиск совпадений', free: '❌', researcher: '✅ Полный', professional: '✅ Полный' },
        { name: 'Защищенное хранилище', free: '❌', researcher: '✅ 1 ГБ', professional: '✅ 10 ГБ' },
        { name: 'Импорт/экспорт', free: '❌', researcher: '✅', professional: '✅' },
        { name: 'Видимость дерева', free: '❌', researcher: '✅ Приватно', professional: '✅ Приватно' },
        { name: 'CRM система', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Аналитика', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Приоритетная поддержка', free: '❌', researcher: '❌', professional: '✅ 24/7' },
      ],
      cta: 'Подписаться',
      ctaLink: '/checkout/researcher'
    },
    {
      name: 'Professional',
      price: '30,000',
      currency: '₽',
      period: '/год',
      description: 'Для профессионалов',
      color: '#faad14',
      features: [
        { name: 'Персон в дереве', free: '50', researcher: '∞', professional: '∞' },
        { name: 'Поиск совпадений', free: '❌', researcher: '✅ Полный', professional: '✅ Полный' },
        { name: 'Защищенное хранилище', free: '❌', researcher: '✅ 1 ГБ', professional: '✅ 10 ГБ' },
        { name: 'Импорт/экспорт', free: '❌', researcher: '✅', professional: '✅' },
        { name: 'Видимость дерева', free: '❌', researcher: '✅ Приватно', professional: '✅ Приватно' },
        { name: 'CRM система', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Аналитика', free: '❌', researcher: '❌', professional: '✅' },
        { name: 'Приоритетная поддержка', free: '❌', researcher: '❌', professional: '✅ 24/7' },
      ],
      cta: 'Подписаться',
      ctaLink: '/checkout/professional'
    }
  ];

  const faqItems = [
    {
      q: 'Какой способ оплаты вы принимаете?',
      a: 'Мы принимаем все основные кредитные карты (Visa, MasterCard, Maestro) через защищенную платежную систему Stripe.'
    },
    {
      q: 'Когда я смогу отменить подписку?',
      a: 'Вы можете отменить подписку в любой момент. Доступ остается до конца оплаченного периода, а затем переходит на Free план.'
    },
    {
      q: 'Могу ли я перейти на другой план?',
      a: 'Да! Вы можете перейти на более высокий или низкий план в любой момент. Плата пересчитается пропорционально.'
    },
    {
      q: 'Есть ли скидка за годовую подписку?',
      a: 'Да! Годовая подписка дешевле, чем оплата по месяцам. Вы экономите примерно 30% при годовом плане.'
    },
    {
      q: 'Что происходит с моими данными, если я отмену подписку?',
      a: 'Ваши данные остаются в безопасности. При переходе на Free план вы сможете работать с первыми 50 персонами, остальные будут заморожены.'
    },
    {
      q: 'Предоставляете ли вы пробный период?',
      a: 'Да! Первые 7 дней подписки Researcher полностью бесплатны. Отмените в любой момент без дополнительных платежей.'
    }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa', padding: '40px 20px' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '60px' }}>
        <h1 style={{ fontSize: '42px', marginBottom: '16px' }}>
          💰 Прозрачное ценообразование
        </h1>
        <p style={{ fontSize: '18px', color: '#666' }}>
          Выберите план, который подходит вам лучше всего. Никаких скрытых платежей.
        </p>
      </div>

      {/* Pricing Cards */}
      <div style={{ maxWidth: '1200px', margin: '0 auto 80px' }}>
        <Row gutter={[24, 24]}>
          {plans.map((plan, index) => (
            <Col key={index} xs={24} md={8}>
              <Card
                hoverable
                style={{
                  height: '100%',
                  border: plan.popular ? `3px solid ${plan.color}` : '1px solid #ddd',
                  position: 'relative'
                }}
              >
                {plan.popular && (
                  <div
                    style={{
                      position: 'absolute',
                      top: '-20px',
                      left: '50%',
                      transform: 'translateX(-50%)',
                      background: plan.color,
                      color: 'white',
                      padding: '8px 16px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}
                  >
                    ⭐ ПОПУЛЯРНЫЙ
                  </div>
                )}

                <h2 style={{ marginBottom: '8px' }}>{plan.name}</h2>
                <p style={{ color: '#666', marginBottom: '24px' }}>
                  {plan.description}
                </p>

                <div style={{ marginBottom: '24px' }}>
                  <span style={{ fontSize: '42px', fontWeight: 'bold', color: plan.color }}>
                    {plan.price}
                  </span>
                  <span style={{ fontSize: '16px', color: '#666' }}>
                    {' '}{plan.currency}{plan.period}
                  </span>
                </div>

                <Button
                  type={plan.popular ? 'primary' : 'default'}
                  size="large"
                  block
                  style={plan.popular ? { background: plan.color, borderColor: plan.color } : {}}
                  onClick={() => window.location.href = plan.ctaLink}
                >
                  {plan.cta}
                </Button>

                <hr style={{ margin: '24px 0' }} />

                <div style={{ fontSize: '12px', color: '#999' }}>
                  Основные функции:
                  {plan.name === 'Free' && (
                    <>
                      <div>✅ До 50 персон</div>
                      <div>✅ Базовый интерфейс</div>
                      <div>❌ Поиск совпадений</div>
                    </>
                  )}
                  {plan.name === 'Researcher' && (
                    <>
                      <div>✅ Неограниченные персоны</div>
                      <div>✅ Полный поиск совпадений</div>
                      <div>✅ Импорт/Экспорт</div>
                    </>
                  )}
                  {plan.name === 'Professional' && (
                    <>
                      <div>✅ Все из Researcher</div>
                      <div>✅ CRM система</div>
                      <div>✅ Приоритетная поддержка</div>
                    </>
                  )}
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* Comparison Table */}
      <div style={{ maxWidth: '1200px', margin: '0 auto 80px', background: 'white', padding: '40px', borderRadius: '8px' }}>
        <h2 style={{ marginBottom: '32px', textAlign: 'center' }}>
          📊 Сравнение функций
        </h2>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ textAlign: 'left', padding: '16px' }}>Функция</th>
                <th style={{ textAlign: 'center', padding: '16px' }}>Free</th>
                <th style={{ textAlign: 'center', padding: '16px', background: '#f5f7fa' }}>Researcher</th>
                <th style={{ textAlign: 'center', padding: '16px' }}>Professional</th>
              </tr>
            </thead>
            <tbody>
              {[
                { name: 'Максимум персон', free: '50', researcher: '∞', prof: '∞' },
                { name: 'Поиск совпадений', free: false, researcher: true, prof: true },
                { name: 'Защищенное хранилище', free: false, researcher: '1 ГБ', prof: '10 ГБ' },
                { name: 'Импорт/Экспорт GEDCOM', free: false, researcher: true, prof: true },
                { name: 'CRM система', free: false, researcher: false, prof: true },
                { name: 'Аналитика и отчеты', free: false, researcher: false, prof: true },
                { name: 'Обновление профиля', free: true, researcher: true, prof: true },
                { name: 'Электронная поддержка', free: true, researcher: true, prof: true },
                { name: 'Приоритетная поддержка 24/7', free: false, researcher: false, prof: true },
              ].map((row, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '16px', fontWeight: 'bold' }}>{row.name}</td>
                  <td style={{ textAlign: 'center', padding: '16px' }}>
                    {typeof row.free === 'boolean' ? (
                      row.free ? <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '18px' }} /> :
                        <CloseCircleOutlined style={{ color: '#d9d9d9', fontSize: '18px' }} />
                    ) : row.free}
                  </td>
                  <td style={{ textAlign: 'center', padding: '16px', background: '#f5f7fa' }}>
                    {typeof row.researcher === 'boolean' ? (
                      row.researcher ? <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '18px' }} /> :
                        <CloseCircleOutlined style={{ color: '#d9d9d9', fontSize: '18px' }} />
                    ) : row.researcher}
                  </td>
                  <td style={{ textAlign: 'center', padding: '16px' }}>
                    {typeof row.prof === 'boolean' ? (
                      row.prof ? <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '18px' }} /> :
                        <CloseCircleOutlined style={{ color: '#d9d9d9', fontSize: '18px' }} />
                    ) : row.prof}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* FAQ Section */}
      <div style={{ maxWidth: '800px', margin: '0 auto 80px' }}>
        <h2 style={{ marginBottom: '32px', textAlign: 'center', fontSize: '32px' }}>
          ❓ Часто задаваемые вопросы
        </h2>

        <div style={{ background: 'white', padding: '0', borderRadius: '8px', overflow: 'hidden' }}>
          {faqItems.map((item, idx) => (
            <div
              key={idx}
              style={{
                borderBottom: idx < faqItems.length - 1 ? '1px solid #eee' : 'none',
                padding: '24px'
              }}
            >
              <h4 style={{ marginBottom: '12px', color: '#1890ff' }}>
                {item.q}
              </h4>
              <p style={{ color: '#666', margin: 0 }}>
                {item.a}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div style={{
        background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
        color: 'white',
        padding: '60px 20px',
        textAlign: 'center',
        borderRadius: '8px',
        maxWidth: '800px',
        margin: '0 auto'
      }}>
        <h2 style={{ marginBottom: '16px' }}>🚀 Готовы начать?</h2>
        <p style={{ marginBottom: '24px', fontSize: '16px' }}>
          Первые 50 персон совершенно бесплатны. Никаких кредитных карт для регистрации.
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
      </div>
    </div>
  );
};

export default Pricing;
