#!/bin/bash

# Скрипт установки и инициализации проекта Семейные корни

set -e

echo "🌳 Инициализация проекта Семейные корни..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cp .env.example .env
    echo "✓ .env файл создан. Пожалуйста, отредактируйте его с вашими данными."
fi

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p backend/app/routes
mkdir -p backend/app/models
mkdir -p backend/app/services
mkdir -p backend/app/db
mkdir -p frontend/src/pages
mkdir -p frontend/src/components
mkdir -p bots/telegram_bot
mkdir -p bots/vk_bot
mkdir -p tests

# Запуск Docker Compose
echo "🐳 Запуск Docker контейнеров..."
docker-compose up -d

# Ожидание инициализации БД
echo "⏳ Ожидание инициализации баз данных..."
sleep 10

# Инициализация базы PostgreSQL
echo "🗄️ Инициализация PostgreSQL..."
docker-compose exec -T postgres psql -U user -c "CREATE DATABASE family_roots;" 2>/dev/null || true

# Инициализация Neo4j
echo "📊 Инициализация Neo4j..."
docker-compose logs neo4j | grep -q "Started" && echo "✓ Neo4j готов" || echo "⚠️ Neo4j инициализируется"

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📍 Адреса приложений:"
echo "   🌐 Frontend:  http://localhost:3000"
echo "   🔌 Backend:   http://localhost:8000"
echo "   📊 Neo4j:     http://localhost:7474"
echo "   🗄️ PostgreSQL: localhost:5432"
echo ""
echo "🚀 Для остановки контейнеров: docker-compose down"
echo "📚 Для просмотра логов: docker-compose logs -f backend"
