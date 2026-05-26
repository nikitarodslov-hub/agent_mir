.PHONY: help install up down logs shell test lint format clean migrate seed

help:
	@echo "🌳 Семейные корни - Команды управления проектом"
	@echo ""
	@echo "Установка и запуск:"
	@echo "  make install      - Инициализация проекта"
	@echo "  make up           - Запустить контейнеры"
	@echo "  make down         - Остановить контейнеры"
	@echo "  make restart      - Перезапустить контейнеры"
	@echo ""
	@echo "Разработка:"
	@echo "  make logs         - Показать логи"
	@echo "  make shell        - Вход в shell backend"
	@echo "  make migrate      - Миграция БД"
	@echo "  make seed         - Заполнение тестовыми данными"
	@echo ""
	@echo "Качество кода:"
	@echo "  make test         - Запустить тесты"
	@echo "  make lint         - Проверка кода"
	@echo "  make format       - Форматирование кода"
	@echo ""
	@echo "Очистка:"
	@echo "  make clean        - Очистить все"

install:
	@bash scripts/setup.sh

up:
	docker-compose up -d
	@echo "✅ Контейнеры запущены"

down:
	docker-compose down
	@echo "✅ Контейнеры остановлены"

restart:
	docker-compose restart
	@echo "✅ Контейнеры перезапущены"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-neo4j:
	docker-compose logs -f neo4j

shell:
	docker-compose exec backend /bin/bash

shell-db:
	docker-compose exec postgres psql -U user -d family_roots

migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python -m scripts.seed_data

test:
	docker-compose exec backend pytest

test-coverage:
	docker-compose exec backend pytest --cov=app

lint:
	docker-compose exec backend flake8 app
	docker-compose exec backend mypy app

format:
	docker-compose exec backend black app
	docker-compose exec backend isort app

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Проект очищен"

build:
	docker-compose build

build-backend:
	docker-compose build backend

build-frontend:
	docker-compose build frontend

reset-db:
	docker-compose exec postgres psql -U user -c "DROP DATABASE family_roots;" 2>/dev/null || true
	docker-compose exec postgres psql -U user -c "CREATE DATABASE family_roots;"
	@echo "✅ База данных пересоздана"

backup-db:
	docker-compose exec postgres pg_dump -U user family_roots > backup-$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Резервная копия создана"

status:
	docker-compose ps

health:
	@echo "Проверка здоровья приложения..."
	@curl -s http://localhost:8000/health | jq .
	@echo ""

deploy:
	@echo "🚀 Подготовка к продакшену..."
	docker-compose -f docker-compose.yml build
	@echo "✅ Готово к развертыванию"
