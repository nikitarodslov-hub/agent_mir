# Архитектура платформы "Семейные корни"

## Структура проекта

```
family-roots/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── person.py
│   │   │   └── relationship.py
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   ├── genealogy.py
│   │   │   ├── fuzzy_matching.py
│   │   │   └── graph_engine.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── tree.py
│   │   │   ├── search.py
│   │   │   └── analytics.py
│   │   └── db/
│   │       ├── postgres.py
│   │       └── neo4j_client.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── bots/
│   ├── telegram_bot/
│   │   └── main.py
│   └── vk_bot/
│       └── main.py
├── docker-compose.yml
└── README.md
```

## Технологический стек

- **Backend**: FastAPI, Python 3.11
- **Frontend**: React.js, TypeScript, D3.js для визуализации
- **БД**: Neo4j (графовая), PostgreSQL (метаданные)
- **Боты**: python-telegram-bot, vk_api
- **Инфраструктура**: Docker, Docker Compose
- **Облако**: Reg.ru, nginx
- **Аутентификация**: JWT

## Основные компоненты

1. **Graph Engine** - вычислительное ядро на Neo4j
2. **Fuzzy Matching** - алгоритм нечеткого поиска
3. **Visualization Engine** - отрисовка деревьев D3.js
4. **Gamification** - квесты, достижения
5. **Telegram/VK боты** - привлечение пользователей
6. **Admin Panel** - управление платформой
