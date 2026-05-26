# ⚡ Быстрый старт - Семейные корни

## 🚀 За 5 минут до запуска приложения

### Шаг 1: Клонирование и подготовка

```bash
cd family-roots
cp .env.example .env
```

### Шаг 2: Запуск контейнеров

```bash
docker-compose up -d
```

Это запустит:
- ✅ PostgreSQL - для метаданных
- ✅ Neo4j - для генеалогических данных  
- ✅ Redis - для кеша
- ✅ FastAPI backend
- ✅ React frontend
- ✅ Telegram и VK боты
- ✅ Nginx reverse proxy

### Шаг 3: Открытие приложения

Откройте в браузере: **http://localhost:3000**

Администратор/разработка: **http://localhost:8000/docs**

## 📋 Основные команды

```bash
# Просмотр логов
docker-compose logs -f backend

# Вход в shell backend контейнера
docker-compose exec backend bash

# Запуск тестов
docker-compose exec backend pytest

# Остановка контейнеров
docker-compose down

# Очистка всего
docker-compose down -v
rm -rf .env
```

## 🎨 Использование Makefile

```bash
make help        # Показать все команды
make up          # Запустить контейнеры
make down        # Остановить контейнеры
make logs        # Показать логи
make test        # Запустить тесты
make clean       # Очистить всё
```

## 🔑 Тестовые учетные данные

```
Email:    test@familyroots.ru
Password: test123456
```

### Администратор
```
Email:    admin@familyroots.ru
Password: admin123456
```

## 🗂️ Файлы конфигурации

| Файл | Описание |
|------|---------|
| `.env` | Переменные окружения |
| `docker-compose.yml` | Конфигурация Docker контейнеров |
| `backend/requirements.txt` | Python зависимости |
| `frontend/package.json` | Node.js зависимости |
| `nginx.conf` | Конфигурация Nginx |

## 📊 API документация

После запуска доступна по адресу:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Решение типичных проблем

### "Port 8000 is already in use"
```bash
# Узнать какой процесс использует порт
lsof -i :8000

# Убить процесс (Linux/Mac)
kill -9 <PID>

# Или выбрать другой порт в docker-compose.yml
```

### "Cannot connect to Docker"
```bash
# Убедитесь что Docker запущен
docker --version
docker-compose --version

# На Linux может потребоваться sudo
sudo docker-compose up -d
```

### "Database connection error"
```bash
# Перезагрузить контейнеры
docker-compose restart postgres neo4j

# Проверить статус
docker-compose logs postgres
```

## 📚 Следующие шаги

1. **Изучение кода**: Начните с `backend/app/main.py`
2. **Добавление функции**: Смотрите примеры в `backend/app/routes/`
3. **UI компоненты**: `frontend/src/pages/`
4. **Тесты**: `backend/tests/`

## 🎯 Примеры запросов API

### Регистрация
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

### Добавить персону
```bash
curl -X POST http://localhost:8000/api/v1/genealogy/persons \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ivan Petrov",
    "birth_date": "1880-01-15",
    "birthplace": "Ufa",
    "gender": "M"
  }'
```

### Поиск
```bash
curl http://localhost:8000/api/v1/search/by-name?q=Ivan
```

## 🔗 Полезные ссылки

- 📖 [Полная документация](README.md)
- 🏗️ [Архитектура проекта](docs/ARCHITECTURE.md)
- 📊 [API документация](docs/API.md)
- 🚀 [Гайд развертывания](docs/DEPLOYMENT.md)
- 🤝 [Contributing guide](CONTRIBUTING.md)

## 💬 Поддержка

- 🐛 Найденные баги: GitHub Issues
- 💡 Идеи: Discussions
- 📧 Email: support@familyroots.ru

---

**Готовы начать?** Запустите `docker-compose up -d` и откройте http://localhost:3000! 🎉
