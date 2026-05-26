# 💰 Монетизация платформы "Семейные корни"

Полное руководство по настройке платежей и монетизации.

## 🎯 Модель дохода

### Три основных тарифа:

1. **Free (Бесплатный)**
   - До 50 персон
   - Базовые функции
   - Ограниченный поиск
   - Цена: $0/месяц

2. **Researcher (Исследователь)** ⭐ ОСНОВНОЙ
   - Неограниченные персоны
   - Полный Fuzzy Matching
   - Защищенное хранилище
   - Импорт/экспорт
   - Цена: 2,490 ₽/год ($26 USD)

3. **Professional (Профессионал)**
   - Все из Researcher
   - CRM система
   - Аналитика
   - Поддержка
   - Цена: 30,000 ₽/год ($315 USD)

## 💳 Интеграция платежных систем

### Вариант 1: Stripe (РЕКОМЕНДУЕТСЯ)

**Почему Stripe?**
- ✅ Принимает карты из РФ через VPN/proxy
- ✅ Работает с рублями
- ✅ Низкие комиссии (2.2% + $0.30)
- ✅ Встроенные биллинг системы
- ✅ Простая интеграция

#### Шаг 1: Создать аккаунт

1. Перейти на https://stripe.com
2. Создать аккаунт в Stripe
3. Пройти верификацию
4. Получить API ключи

#### Шаг 2: Интеграция в приложение

```bash
pip install stripe
```

```python
# backend/app/services/payment.py
import stripe
from typing import Dict, Optional

class StripePaymentService:
    def __init__(self, api_key: str):
        stripe.api_key = api_key
        
    def create_subscription(
        self,
        customer_email: str,
        plan_id: str,
        user_id: str
    ) -> Dict:
        """Создать подписку"""
        try:
            # Создать customer
            customer = stripe.Customer.create(
                email=customer_email,
                metadata={"user_id": user_id}
            )
            
            # Создать subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": plan_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )
            
            return {
                "status": "success",
                "subscription_id": subscription.id,
                "customer_id": customer.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }
        except stripe.error.StripeError as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def cancel_subscription(self, subscription_id: str) -> Dict:
        """Отменить подписку"""
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return {
                "status": "success",
                "message": "Subscription canceled"
            }
        except stripe.error.StripeError as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_subscription(self, subscription_id: str) -> Dict:
        """Получить информацию о подписке"""
        subscription = stripe.Subscription.retrieve(subscription_id)
        return {
            "id": subscription.id,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end,
            "plan": subscription.items.data[0].price.id
        }
```

#### Шаг 3: API маршрут для платежей

```python
# backend/app/routes/payments.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class SubscriptionRequest(BaseModel):
    plan_id: str  # price_monthly_researcher, price_yearly_professional
    email: str

@router.post("/subscribe")
async def create_subscription(
    request: SubscriptionRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """Создать подписку"""
    try:
        payment_service = StripePaymentService(settings.STRIPE_API_KEY)
        result = payment_service.create_subscription(
            request.email,
            request.plan_id,
            current_user_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Webhook для Stripe событий"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400)
    
    # Обработать события
    if event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        user_id = subscription["metadata"]["user_id"]
        
        # Обновить статус подписки в БД
        update_user_subscription(
            user_id,
            subscription["id"],
            subscription["status"]
        )
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        user_id = subscription["metadata"]["user_id"]
        
        # Обновить статус на бесплатный
        update_user_subscription(user_id, None, "canceled")
    
    return {"status": "success"}
```

### Вариант 2: Яндекс.Касса / ЮКасса (АЛЬТЕРНАТИВА)

```python
# backend/app/services/yookassa_payment.py
import yookassa
from yookassa import Client, Payment

class YooKassaPaymentService:
    def __init__(self, shop_id: str, api_key: str):
        Client.auth(shop_id, api_key)
        self.shop_id = shop_id
    
    def create_payment(
        self,
        amount: float,
        description: str,
        user_id: str
    ) -> Dict:
        """Создать платеж через ЮКассу"""
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://familyroots.ru/payment-success"
            },
            "description": description,
            "metadata": {
                "user_id": user_id
            }
        }, uuid.uuid4())
        
        return {
            "payment_id": payment.id,
            "confirmation_url": payment.confirmation.confirmation_url,
            "status": payment.status
        }
```

### Вариант 3: Сбербанк / Альфа-Банк (для РФ)

```python
# Использовать готовые SDK:
# - https://github.com/sberbank-ai/acquiring-sdk-python
# - https://github.com/alfacash/acquiring-sdk
```

## 📱 Frontend интеграция платежей

```typescript
// frontend/src/services/payment.ts
import axios from 'axios';

export const paymentService = {
  async createSubscription(planId: string, email: string) {
    const response = await axios.post(
      `${process.env.REACT_APP_API_URL}/payments/subscribe`,
      { plan_id: planId, email },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
    
    // Redirect на Stripe Payment Sheet
    if (response.data.status === 'success') {
      window.location.href = response.data.confirmation_url;
    }
  },
  
  async getSubscriptionStatus() {
    const response = await axios.get(
      `${process.env.REACT_APP_API_URL}/payments/subscription`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    );
    return response.data;
  }
};
```

## 🛍️ Страница подписки

```typescript
// frontend/src/pages/Subscription.tsx
import React, { useState } from 'react';
import { Card, Button, Row, Col, Table, Tag, Modal } from 'antd';
import { CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';

const Subscription: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const plans = [
    {
      name: 'Free',
      price: '0',
      currency: '₽',
      features: [
        'До 50 персон',
        'Базовый поиск',
        '-',
        '-'
      ],
      popular: false
    },
    {
      name: 'Researcher',
      price: '2,490',
      currency: '₽/год',
      features: [
        'Неограниченные персоны',
        'Полный Fuzzy Matching',
        'Защищенное хранилище',
        'Импорт/экспорт'
      ],
      popular: true,
      planId: 'price_yearly_researcher'
    },
    {
      name: 'Professional',
      price: '30,000',
      currency: '₽/год',
      features: [
        'Все из Researcher',
        'CRM система',
        'Аналитика',
        'Приоритетная поддержка'
      ],
      popular: false,
      planId: 'price_yearly_professional'
    }
  ];

  const handleSubscribe = async (planId: string) => {
    setLoading(true);
    try {
      await paymentService.createSubscription(planId, 'user@example.com');
    } catch (error) {
      console.error('Subscription error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '48px 0' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '48px' }}>
        💳 Выберите подписку
      </h1>

      <Row gutter={24}>
        {plans.map((plan) => (
          <Col key={plan.name} xs={24} md={8} style={{ marginBottom: '24px' }}>
            <Card
              style={{
                border: plan.popular ? '2px solid #1890ff' : '1px solid #ddd',
                height: '100%'
              }}
              hoverable
            >
              {plan.popular && (
                <div
                  style={{
                    position: 'absolute',
                    top: '-12px',
                    right: '20px',
                    background: '#1890ff',
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 'bold'
                  }}
                >
                  ПОПУЛЯРНЫЙ
                </div>
              )}

              <h2>{plan.name}</h2>
              <div style={{ marginBottom: '24px' }}>
                <span style={{ fontSize: '32px', fontWeight: 'bold' }}>
                  {plan.price}
                </span>
                <span style={{ fontSize: '16px', color: '#666' }}>
                  {' '}{plan.currency}
                </span>
              </div>

              <div style={{ marginBottom: '24px' }}>
                {plan.features.map((feature, i) => (
                  <div key={i} style={{ marginBottom: '8px' }}>
                    <CheckCircleOutlined style={{ color: '#52c41a', marginRight: '8px' }} />
                    {feature}
                  </div>
                ))}
              </div>

              <Button
                type={plan.popular ? 'primary' : 'default'}
                size="large"
                block
                loading={loading}
                onClick={() => handleSubscribe(plan.planId)}
                disabled={!plan.planId}
              >
                {plan.planId ? 'Подписаться' : 'Текущий план'}
              </Button>
            </Card>
          </Col>
        ))}
      </Row>

      <Card style={{ marginTop: '48px' }} title="❓ Часто задаваемые вопросы">
        <div style={{ marginBottom: '16px' }}>
          <h4>Когда я смогу отменить подписку?</h4>
          <p>В любой момент, без штрафов. Подписка будет активна до конца оплаченного периода.</p>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <h4>Какой способ оплаты вы принимаете?</h4>
          <p>Мы принимаем карты Visa, MasterCard, Maestro и другие платежные системы через Stripe.</p>
        </div>

        <div>
          <h4>Нужно ли добавлять способ оплаты для Free плана?</h4>
          <p>Нет, Free план полностью бесплатен и не требует платежных данных.</p>
        </div>
      </Card>
    </div>
  );
};

export default Subscription;
```

## 📊 Аналитика и отчеты

```python
# backend/app/services/analytics.py
class SubscriptionAnalytics:
    def get_revenue(self, period: str = "month") -> Dict:
        """Получить доход"""
        # SELECT SUM(amount) FROM payments WHERE status='success'
        pass
    
    def get_churn_rate(self) -> float:
        """Процент отмен подписок"""
        # Canceled subscriptions / Total subscriptions
        pass
    
    def get_mrr(self) -> float:
        """Monthly Recurring Revenue"""
        # Доход от текущих активных подписок
        pass
    
    def get_arr(self) -> float:
        """Annual Recurring Revenue"""
        # MRR * 12
        pass
```

## 🎁 Промо-коды и скидки

```python
# backend/app/routes/promos.py
@router.post("/apply-promo")
async def apply_promo(
    promo_code: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Применить промо-код"""
    promo = db.query(PromoCode).filter_by(code=promo_code).first()
    
    if not promo or promo.expired:
        raise HTTPException(status_code=404, detail="Invalid promo code")
    
    # Применить скидку
    user = db.query(User).get(current_user_id)
    user.discount = promo.discount_percent
    db.commit()
    
    return {"status": "success", "discount": promo.discount_percent}
```

## 📈 Стратегии роста доходов

### 1. Реферальная программа
```python
# Пригласи друга - получи скидку 20%
# За каждого приглашенного - бонус $5
```

### 2. Годовая подписка со скидкой
```python
Monthly: 299₽ = 3,588₽/год
Yearly:  2,490₽ = Скидка 31% ✅
```

### 3. Team лицензии
```python
Professional Pro: 500,000₽/год для команд 10+ человек
```

### 4. API доступ
```python
Developer API: 50,000₽/месяц
Интеграция с другими системами
```

### 5. Консультации
```python
1 час консультации генеалога: 5,000₽
Доступ через платформу
```

## 💡 Tips для успеха

1. **Начните с бесплатного плана** - снизит barrier to entry
2. **Годовая скидка 30-40%** - стимулирует долгосрочные подписки
3. **Бесплатный пробный период 7 дней** - увеличит конверсию
4. **Отправляйте email напоминания** перед окончанием пробного периода
5. **Показывайте ценность** - кейсы, отзывы, статистика
6. **A/B тестируйте цены** - найдите оптимальный price point

## 📞 Финальная чек-лист

- ✅ Выбрать платежную систему (Stripe/ЮКасса)
- ✅ Создать аккаунт и получить API ключи
- ✅ Интегрировать в backend
- ✅ Создать страницу подписки на frontend
- ✅ Настроить webhook для обработки платежей
- ✅ Добавить отправку email уведомлений
- ✅ Протестировать платежный процесс
- ✅ Запустить в production
- ✅ Мониторить конверсию и отмены

---

**Платформа готова к монетизации!** 💰🎉
