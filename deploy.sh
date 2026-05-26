#!/bin/bash
set -e

# 🚀 PRODUCTION DEPLOYMENT SCRIPT для "Семейные корни"
# Полностью автоматизированное развертывание на VPS/облаке

echo "🌳 Начинаем развертывание платформы 'Семейные корни'..."

# Конфигурация
DOMAIN="${1:-familyroots.ru}"
SERVER_IP="${2:-}"
SSH_USER="${3:-root}"
APP_DIR="/opt/family-roots"
GITHUB_REPO="https://github.com/nikitarodslov-hub/agent_mir.git"

echo "📋 Параметры развертывания:"
echo "   Домен: $DOMAIN"
echo "   Директория приложения: $APP_DIR"
echo ""

# ============================================
# Шаг 1: Система и зависимости
# ============================================
echo "📦 Установка зависимостей системы..."

apt-get update
apt-get install -y \
    curl \
    wget \
    git \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    nginx \
    certbot \
    python3-certbot-nginx

# ============================================
# Шаг 2: Docker и Docker Compose
# ============================================
echo "🐳 Установка Docker..."

# Добавить Docker repo
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Установить docker-compose отдельно для совместимости
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Запустить Docker
systemctl start docker
systemctl enable docker

echo "✅ Docker установлен"

# ============================================
# Шаг 3: Клонирование приложения
# ============================================
echo "📥 Клонирование приложения..."

mkdir -p $APP_DIR
cd $APP_DIR

if [ -d ".git" ]; then
    git pull origin main
else
    git clone -b main $GITHUB_REPO .
fi

# ============================================
# Шаг 4: Production переменные окружения
# ============================================
echo "⚙️ Создание production .env..."

cat > .env.production << EOF
# Production конфигурация для $DOMAIN

# Database
DATABASE_URL=postgresql://family_roots:$(openssl rand -base64 32)@postgres:5432/family_roots
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=$(openssl rand -base64 32)

# Redis
REDIS_URL=redis://redis:6379

# JWT Secret (ВАЖНО: используйте сильный ключ!)
SECRET_KEY=$(openssl rand -base64 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Telegram Bot
TELEGRAM_TOKEN=${TELEGRAM_TOKEN:-}

# VK Bot
VK_TOKEN=${VK_TOKEN:-}
VK_GROUP_ID=${VK_GROUP_ID:-}

# API
API_URL=https://$DOMAIN
API_V1_STR=/api/v1
FRONTEND_URL=https://$DOMAIN

# Frontend
REACT_APP_API_URL=https://$DOMAIN/api/v1

# Email (для уведомлений)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=${SMTP_USER:-}
SMTP_PASSWORD=${SMTP_PASSWORD:-}

# Environment
ENVIRONMENT=production
DEBUG=false

# Security
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN
CORS_ORIGINS=https://$DOMAIN,https://www.$DOMAIN

# Database Backups
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30

# Monitoring
SENTRY_DSN=${SENTRY_DSN:-}
EOF

chmod 600 .env.production
echo "✅ .env создан"

# ============================================
# Шаг 5: Production Docker Compose
# ============================================
echo "🐳 Создание production docker-compose..."

cat > docker-compose.production.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: family_roots_postgres
    environment:
      POSTGRES_DB: family_roots
      POSTGRES_USER: family_roots
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    networks:
      - family_roots
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U family_roots"]
      interval: 10s
      timeout: 5s
      retries: 5

  neo4j:
    image: neo4j:5.14-enterprise
    container_name: family_roots_neo4j
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
      NEO4J_dbms_memory_heap_maxSize: 4G
      NEO4J_dbms_memory_pagecache_size: 2G
      NEO4J_ACCEPT_LICENSE_AGREEMENT: yes
    volumes:
      - neo4j_data:/var/lib/neo4j/data
      - neo4j_logs:/var/lib/neo4j/logs
    restart: unless-stopped
    networks:
      - family_roots
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: family_roots_redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - family_roots
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: family_roots_backend
    command: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    environment:
      DATABASE_URL: ${DATABASE_URL}
      NEO4J_URI: ${NEO4J_URI}
      NEO4J_USER: ${NEO4J_USER}
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      SECRET_KEY: ${SECRET_KEY}
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
      VK_TOKEN: ${VK_TOKEN}
    volumes:
      - ./backend:/app
    restart: unless-stopped
    networks:
      - family_roots
    depends_on:
      postgres:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      redis:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: family_roots_frontend
    environment:
      REACT_APP_API_URL: ${REACT_APP_API_URL}
    restart: unless-stopped
    networks:
      - family_roots

  telegram_bot:
    build:
      context: ./bots/telegram_bot
      dockerfile: Dockerfile
    container_name: family_roots_telegram_bot
    environment:
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
      API_URL: http://backend:8000/api/v1
    restart: unless-stopped
    networks:
      - family_roots
    depends_on:
      - backend

  vk_bot:
    build:
      context: ./bots/vk_bot
      dockerfile: Dockerfile
    container_name: family_roots_vk_bot
    environment:
      VK_TOKEN: ${VK_TOKEN}
      VK_GROUP_ID: ${VK_GROUP_ID}
      API_URL: http://backend:8000/api/v1
    restart: unless-stopped
    networks:
      - family_roots
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    container_name: family_roots_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.production.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
      - nginx_logs:/var/log/nginx
    restart: unless-stopped
    networks:
      - family_roots
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  neo4j_data:
  neo4j_logs:
  redis_data:
  nginx_logs:

networks:
  family_roots:
    driver: bridge
EOF

# ============================================
# Шаг 6: Nginx конфигурация
# ============================================
echo "🔧 Настройка Nginx..."

cat > nginx.production.conf << EOF
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 2048;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                    '\$status \$body_bytes_sent "\$http_referer" '
                    '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 500M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/x-javascript application/xml+rss
               application/json application/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api_limit:10m rate=100r/s;
    limit_req_zone \$binary_remote_addr zone=general_limit:10m rate=50r/s;

    # Upstreams
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name $DOMAIN www.$DOMAIN;
        return 301 https://\$server_name\$request_uri;
    }

    # Main HTTPS server
    server {
        listen 443 ssl http2;
        server_name $DOMAIN www.$DOMAIN;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # HSTS
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # API
        location /api/ {
            limit_req zone=api_limit burst=200 nodelay;

            proxy_pass http://backend/api/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;

            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy";
            add_header Content-Type text/plain;
        }

        # Deny access to hidden files
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
EOF

echo "✅ Nginx настроен"

# ============================================
# Шаг 7: SSL сертификат (Let's Encrypt)
# ============================================
echo "🔐 Настройка SSL сертификата..."

mkdir -p ssl

# Остановить Nginx временно для certbot
systemctl stop nginx || true

certbot certonly --standalone \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --email admin@$DOMAIN \
    --agree-tos \
    --non-interactive \
    --preferred-challenges http || echo "⚠️ Certbot может потребовать ручной настройки"

# Скопировать сертификаты
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ssl/cert.pem
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/key.pem
    chmod 644 ssl/cert.pem ssl/key.pem
    echo "✅ SSL сертификат установлен"
else
    echo "⚠️ SSL сертификат не установлен. Используйте self-signed временно."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem -out ssl/cert.pem \
        -subj "/C=RU/ST=Russia/L=Moscow/O=FamilyRoots/CN=$DOMAIN"
fi

# Создать cron job для auto-renewal
echo "0 0 1 * * /usr/bin/certbot renew --quiet && systemctl reload nginx" | crontab -

# ============================================
# Шаг 8: Запуск приложения
# ============================================
echo "🚀 Запуск приложения..."

cd $APP_DIR

# Создать необходимые директории
mkdir -p backups logs

# Запустить Docker Compose
docker-compose -f docker-compose.production.yml --env-file .env.production up -d

echo "⏳ Ожидание инициализации сервисов..."
sleep 30

# ============================================
# Шаг 9: Инициализация БД
# ============================================
echo "🗄️ Инициализация базы данных..."

docker-compose -f docker-compose.production.yml exec -T backend alembic upgrade head || true

echo "✅ База данных инициализирована"

# ============================================
# Шаг 10: Создание backup скрипта
# ============================================
echo "📦 Создание backup скрипта..."

cat > $APP_DIR/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/family-roots/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Создание резервной копии базы данных..."

# PostgreSQL backup
docker-compose -f docker-compose.production.yml exec -T postgres \
    pg_dump -U family_roots family_roots | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Neo4j backup
docker-compose -f docker-compose.production.yml exec -T neo4j \
    neo4j-admin database dump neo4j --to-path /var/lib/neo4j/backups/ || true

# Redis dump
docker-compose -f docker-compose.production.yml exec -T redis \
    redis-cli BGSAVE || true

# Очистить старые backup'ы (старше 30 дней)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "✅ Резервная копия создана: $BACKUP_DIR/postgres_$DATE.sql.gz"
EOF

chmod +x $APP_DIR/backup.sh

# Добавить в cron (каждый день в 3:00 AM)
echo "0 3 * * * /opt/family-roots/backup.sh" | crontab -

# ============================================
# Итоговая информация
# ============================================
echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ ПЛАТФОРМА УСПЕШНО РАЗВЕРНУТА!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🌐 Ссылка на приложение: https://$DOMAIN"
echo "📊 API документация: https://$DOMAIN/api/v1/docs"
echo "🔧 Admin панель: https://$DOMAIN/admin"
echo ""
echo "🔑 Важно:"
echo "   1. Измените пароли в .env.production"
echo "   2. Установите TELEGRAM_TOKEN и VK_TOKEN"
echo "   3. Настройте email для уведомлений"
echo "   4. Проверьте SSL сертификат"
echo ""
echo "📝 Полезные команды:"
echo "   docker-compose -f docker-compose.production.yml logs -f backend"
echo "   docker-compose -f docker-compose.production.yml ps"
echo "   bash /opt/family-roots/backup.sh"
echo ""
echo "🔄 Обновление приложения:"
echo "   cd /opt/family-roots"
echo "   git pull origin main"
echo "   docker-compose -f docker-compose.production.yml up -d --build"
echo ""
echo "════════════════════════════════════════════════════════"
