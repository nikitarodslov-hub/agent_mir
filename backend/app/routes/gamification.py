"""
API маршруты для геймификации (квесты, достижения)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

router = APIRouter()

class AchievementType(str, Enum):
    FIRST_PERSON = "first_person"
    TEN_PERSONS = "ten_persons"
    HUNDRED_PERSONS = "hundred_persons"
    COMPLETE_TREE = "complete_tree"
    DEEP_RESEARCH = "deep_research"
    FAMILY_HISTORIAN = "family_historian"
    ARCHIVIST = "archivist"
    CONNECTOR = "connector"
    TIMEKEEPER = "timekeeper"

class QuestType(str, Enum):
    FIND_ANCESTORS = "find_ancestors"
    DOCUMENT_CENTURY = "document_century"
    TRACE_MIGRATION = "trace_migration"
    BUILD_TREE = "build_tree"
    VERIFY_RECORDS = "verify_records"

class Achievement(BaseModel):
    id: str
    title: str
    description: str
    icon_url: str
    unlock_date: Optional[datetime] = None
    progress: int = 0
    max_progress: int = 100
    rarity: str  # common, rare, epic, legendary

class Quest(BaseModel):
    id: str
    title: str
    description: str
    quest_type: QuestType
    reward_points: int
    completed: bool
    progress: int
    max_progress: int

@router.get("/achievements")
async def get_achievements(current_user_id: str = Depends(get_current_user_id)):
    """Получить список всех доступных достижений пользователя"""
    try:
        achievements = [
            Achievement(
                id="ach_1",
                title="Первый шаг",
                description="Добавьте вашу первую персону",
                icon_url="https://api.familyroots.ru/icons/first_person.png",
                unlock_date=datetime.utcnow(),
                progress=100,
                max_progress=100,
                rarity="common"
            ),
            Achievement(
                id="ach_2",
                title="Архивист",
                description="Добавьте 100+ персон в ваше дерево",
                icon_url="https://api.familyroots.ru/icons/archivist.png",
                progress=45,
                max_progress=100,
                rarity="rare"
            ),
            Achievement(
                id="ach_3",
                title="Летописец",
                description="Найдите 5 различных веков в вашей истории",
                icon_url="https://api.familyroots.ru/icons/historian.png",
                progress=3,
                max_progress=5,
                rarity="epic"
            )
        ]

        return {
            "status": "success",
            "achievements": achievements,
            "total_points": 850
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/achievements/{achievement_id}")
async def get_achievement_details(
    achievement_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Получить информацию о конкретном достижении"""
    try:
        return {
            "status": "success",
            "achievement": {
                "id": achievement_id,
                "title": "Архивист",
                "description": "Добавьте 100+ персон в ваше дерево",
                "long_description": "Это достижение требует упорства и кропотливой работы с архивами. Добавьте 100 персон, чтобы получить его.",
                "progress": 45,
                "max_progress": 100,
                "reward_points": 500,
                "rarity": "rare",
                "obtained_at": None,
                "tips": [
                    "Используйте массовый импорт из GEDCOM",
                    "Ищите дубликаты автоматически",
                    "Синхронизируйте с известными архивами"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quests")
async def get_active_quests(current_user_id: str = Depends(get_current_user_id)):
    """Получить активные квесты пользователя"""
    try:
        quests = [
            Quest(
                id="quest_1",
                title="Найди своих предков",
                description="Найдите информацию о 3 предках в архивах",
                quest_type=QuestType.FIND_ANCESTORS,
                reward_points=100,
                completed=False,
                progress=1,
                max_progress=3
            ),
            Quest(
                id="quest_2",
                title="Столетний документ",
                description="Найдите запись, которой больше 100 лет",
                quest_type=QuestType.DOCUMENT_CENTURY,
                reward_points=50,
                completed=False,
                progress=0,
                max_progress=1
            ),
            Quest(
                id="quest_3",
                title="След миграции",
                description="Проследите путь миграции вашей семьи",
                quest_type=QuestType.TRACE_MIGRATION,
                reward_points=200,
                completed=False,
                progress=2,
                max_progress=5
            )
        ]

        return {
            "status": "success",
            "quests": quests,
            "total_active": len(quests)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quests/{quest_id}/progress")
async def update_quest_progress(
    quest_id: str,
    increment: int = 1,
    current_user_id: str = Depends(get_current_user_id)
):
    """Обновить прогресс квеста"""
    try:
        return {
            "status": "success",
            "quest_id": quest_id,
            "new_progress": 3,
            "completed": True,
            "reward_claimed": 100
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    period: str = "week"  # week, month, all_time
):
    """Получить таблицу лидеров"""
    try:
        leaderboard = [
            {
                "rank": 1,
                "user_name": "ИванПетров",
                "points": 5420,
                "persons_count": 342,
                "level": 15
            },
            {
                "rank": 2,
                "user_name": "МарияСмирнова",
                "points": 4890,
                "persons_count": 298,
                "level": 14
            },
            {
                "rank": 3,
                "user_name": "АлексейКуранов",
                "points": 4120,
                "persons_count": 256,
                "level": 12
            }
        ]

        return {
            "status": "success",
            "leaderboard": leaderboard,
            "period": period
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user-stats")
async def get_user_stats(current_user_id: str = Depends(get_current_user_id)):
    """Получить персональную статистику пользователя"""
    try:
        return {
            "status": "success",
            "stats": {
                "total_points": 850,
                "level": 7,
                "exp_to_next_level": 450,
                "achievements_unlocked": 8,
                "achievements_total": 25,
                "persons_added": 45,
                "connections_made": 120,
                "quests_completed": 3,
                "days_active": 34,
                "last_activity": datetime.utcnow(),
                "rank": 47,
                "rank_percentile": 92
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/daily-bonus")
async def claim_daily_bonus(current_user_id: str = Depends(get_current_user_id)):
    """Получить ежедневный бонус"""
    try:
        return {
            "status": "success",
            "bonus_points": 10,
            "streak": 5,
            "next_bonus_at": "2024-01-15T10:00:00"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/challenges")
async def get_seasonal_challenges():
    """Получить сезонные вызовы"""
    try:
        return {
            "status": "success",
            "current_season": "Winter 2024",
            "challenges": [
                {
                    "id": "ch_1",
                    "title": "Зимние корни",
                    "description": "Найдите 5 записей, датированных зимними месяцами",
                    "reward_points": 300,
                    "progress": 2,
                    "max_progress": 5,
                    "ends_at": "2024-02-01"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_current_user_id(token: str = None) -> str:
    """Вспомогательная функция для получения ID текущего пользователя"""
    # TODO: Реализовать JWT верификацию
    return "user_123"
