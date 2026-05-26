# 🚀 Развертывание на production домене

Полное руководство по развертыванию платформы "Семейные корни" на собственном домене.

## 📋 Требования

- VPS/Облачный сервер (DigitalOcean, AWS, Linode, Hetzner и т.д.)
- Ubuntu 20.04+ или Debian 11+
- Минимум 4GB RAM и 2 CPU cores
- Собственный домен
- SSH доступ к серверу

## 🎯 Выбор хостинга

### ✅ Рекомендуемые варианты

#### 1. **DigitalOcean** (САМЫЙ ПРОСТОЙ)
- **Стоимость:** $6/месяц за базовый дроплет
- **Плюсы:** Простая настройка, хороший апстрим, CDN включен
- **Минусы:** Немного дороже чем AWS

```bash
# 1. Создать дроплет на DigitalOcean (Ubuntu 22.04)
# 2. Получить IP адрес
# 3. Указать домен на этот IP в DNS
# 4. Подключиться по SSH
ssh root@YOUR_IP
```

#### 2. **AWS Lightsail**
- **Стоимость:** $5/месяц
- **Плюсы:** Масштабируемость, мировые регионы
- **Минусы:** Сложнее настройка

#### 3. **Hetzner**
- **Стоимость:** €3/месяц
- **Плюсы:** Очень дешево, хороший апстрим
- **Минусы:** Служба поддержки на немецком

### 🌍 Конкретный пример: DigitalOcean

## 🔧 Пошаговое развертывание

### Шаг 1: Подготовка сервера

```bash
# Подключиться к серверу
ssh root@YOUR_VPS_IP

# Создать пользователя (не рекомендуется работать под root)
adduser deployer
usermod -aG sudo deployer
usermod -aG docker deployer

# Переключиться на пользователя
su - deployer
```

### Шаг 2: Запуск автоматического развертывания

```bash
# Клонировать репозиторий
git clone https://github.com/nikitarodslov-hub/agent_mir.git
cd agent_mir

# Запустить скрипт развертывания
sudo bash deploy.sh familyroots.ru

# Введите параметры:
# - Домен: familyroots.ru
# - IP сервера: (автоматически определится)
# - SSH пользователь: deployer
```

**Что делает скрипт:**
- ✅ Устанавливает Docker и Docker Compose
- ✅ Клонирует приложение
- ✅ Создает production .env
- ✅ Генерирует SSL сертификат (Let's Encrypt)
- ✅ Настраивает Nginx
- ✅ Запускает все сервисы
- ✅ Создает backup скрипты

### Шаг 3: Настройка DNS

Отправьте домен на IP сервера через панель управления хостинга:

**Тип записи:** A  
**Имя:** @  
**Значение:** YOUR_VPS_IP  

**Для поддомена www:**

**Тип записи:** CNAME  
**Имя:** www  
**Значение:** familyroots.ru  

⏳ **Ждите 5-30 минут пока DNS распространится**

### Шаг 4: Проверка работы

```bash
# Проверить статус контейнеров
docker-compose -f docker-compose.production.yml ps

# Посмотреть логи
docker-compose -f docker-compose.production.yml logs -f backend

# Проверить здоровье приложения
curl https://familyroots.ru/health
```

## 🔑 Финальная конфигурация

### 1. Установить переменные окружения

```bash
# Отредактировать .env.production на сервере
nano /opt/family-roots/.env.production
```

**Обязательно установить:**

```bash
# Telegram Bot (получить у @BotFather в Telegram)
TELEGRAM_TOKEN=123456789:ABCdefGHIjklmnoPQRstUVwxyzABCdefGHI

# VK Bot (получить в разделе VK Apps)
VK_TOKEN=your_vk_token
VK_GROUP_ID=your_group_id

# Email для уведомлений
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # Не обычный пароль!

# Sentry для мониторинга ошибок (опционально)
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 2. Перезагрузить приложение

```bash
cd /opt/family-roots
docker-compose -f docker-compose.production.yml up -d
```

### 3. Проверить приложение

```bash
# Фронтенд
https://familyroots.ru

# API документация
https://familyroots.ru/api/v1/docs

# ReDoc
https://familyroots.ru/api/v1/redoc

# Admin панель
https://familyroots.ru/admin (после добавления маршрута)
```

## 📊 Оптимизация для production

### 1. Кэширование фронтенда

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 2. CDN интеграция

Если у вас много пользователей, подключите Cloudflare:

```bash
1. Перейти на https://cloudflare.com
2. Добавить ваш домен
3. Изменить nameservers у регистратора
4. Включить Auto Minify (CSS, JS, HTML)
5. Включить Brotli compression
6. Установить Page Rules для API
```

### 3. Мониторинг

```bash
# Установить Prometheus + Grafana
docker run -d --name prometheus prom/prometheus

# Или используйте UptimeRobot для health checks
# https://uptimerobot.com (бесплатно для 50 мониторов)
```

### 4. Резервные копии

```bash
# Резервные копии создаются ежедневно в 3:00 AM
# Проверить backup
ls -lah /opt/family-roots/backups/

# Ручное создание backup
bash /opt/family-roots/backup.sh

# Восстановление из backup
gunzip -c backups/postgres_20240101_030000.sql.gz | \
    docker-compose -f docker-compose.production.yml exec -T postgres \
    psql -U family_roots -d family_roots
```

## 🔄 Автоматические обновления

### GitHub Actions CI/CD

Когда вы push код в `main` ветку, автоматически:

1. ✅ Собираются Docker образы
2. ✅ Запускаются тесты
3. ✅ Загружаются на сервер
4. ✅ Перезапускаются контейнеры

**Требуется настроить GitHub Secrets:**

```bash
# Перейти: Settings → Secrets and variables → Actions
# Добавить:

PRODUCTION_HOST = your_server_ip
PRODUCTION_USER = deployer
PRODUCTION_SSH_KEY = (содержимое ~/.ssh/id_rsa)
PRODUCTION_DOMAIN = familyroots.ru
SLACK_WEBHOOK = (опционально для уведомлений)
```

## 🔐 Безопасность

### 1. Firewall

```bash
# Разрешить только необходимые порты
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. SSL сертификат

```bash
# Автоматическое обновление (уже настроено через cron)
# Проверить статус
sudo certbot certificates

# Обновить вручную
sudo certbot renew --force-renewal
```

### 3. Защита от DDoS

```bash
# Cloudflare (бесплатно) или:
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 4. Регулярные обновления

```bash
# Создать скрипт для обновления системы
echo "0 2 * * * sudo apt-get update && sudo apt-get upgrade -y" | crontab -
```

## 📈 Мониторинг и масштабирование

### Когда понадобится больше ресурсов?

- **2k+ активных пользователей:** Перейти на 8GB RAM, 4 CPU
- **5k+ активных пользователей:** Использовать Kubernetes или AWS Auto Scaling
- **10k+:** Отдельные серверы для БД, Redis, приложения

### Мониторинг производительности

```bash
# SSH на сервер
ssh deployer@your_vps

# Посмотреть использование ресурсов
docker stats

# Посмотреть логи ошибок
docker-compose -f docker-compose.production.yml logs backend | grep ERROR

# Проверить объем БД
docker-compose -f docker-compose.production.yml exec postgres \
    psql -U family_roots -c "SELECT pg_size_pretty(pg_database_size('family_roots'))"
```

## 💰 Расходы в месяц

| Компонент | Стоимость |
|-----------|----------|
| VPS (DigitalOcean) | $6-24 |
| Домен | $10-15 |
| SSL (Let's Encrypt) | 0 |
| CDN (Cloudflare) | 0-20 |
| Email (Gmail) | 0 |
| Monitoring (UptimeRobot) | 0-10 |
| **Итого** | **$16-69** |

## 🆘 Решение проблем

### Приложение не запускается

```bash
# Проверить логи
docker-compose logs backend

# Если БД не инициализирована
docker-compose exec backend alembic upgrade head

# Перезагрузить все контейнеры
docker-compose restart
```

### Высокая нагрузка на CPU

```bash
# Увеличить количество worker'ов
# В docker-compose.production.yml найти backend:
# command: gunicorn app.main:app --workers 8  # было 4, увеличить до 8
```

### Заканчивается дисковое пространство

```bash
# Очистить старые логи
docker system prune -a

# Очистить старые backup'ы
find /opt/family-roots/backups -mtime +30 -delete
```

## 📞 Техническая поддержка

- 📧 Email: support@familyroots.ru
- 💬 Telegram: @familyroots_support
- 🐛 GitHub Issues: https://github.com/nikitarodslov-hub/agent_mir/issues

## 📚 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

---

**Поздравляем! Ваша платформа готова к монетизации!** 🎉
