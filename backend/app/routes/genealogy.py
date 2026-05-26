"""
API маршруты для генеалогических операций
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

class PersonCreate(BaseModel):
    name: str
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    birthplace: Optional[str] = None
    gender: str = "U"  # U=Unknown, M=Male, F=Female
    social_class: Optional[str] = None

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    birthplace: Optional[str] = None
    gender: Optional[str] = None
    social_class: Optional[str] = None

class RelationshipCreate(BaseModel):
    person_id_1: str
    person_id_2: str
    relationship_type: str  # PARENT_OF, SPOUSE_OF, SIBLING_OF, CHILD_OF

class TreeResponse(BaseModel):
    person_id: str
    name: str
    depth: int
    ancestors_count: int
    descendants_count: int
    total_relationships: int

@router.post("/persons", response_model=dict)
async def create_person(person: PersonCreate, current_user_id: str = Depends(get_current_user_id)):
    """Создает новую персону в дереве пользователя"""
    try:
        # Получаем граф
        from app.main import graph_engine
        result = await graph_engine.create_person(
            user_id=current_user_id,
            name=person.name,
            birth_date=person.birth_date,
            death_date=person.death_date,
            birthplace=person.birthplace,
            gender=person.gender
        )
        return {
            "status": "success",
            "person": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/persons/{person_id}")
async def get_person(person_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Получает информацию о персоне"""
    try:
        # TODO: Получить из Neo4j
        return {
            "id": person_id,
            "name": "Sample Person",
            "birth_date": "1980-01-01",
            "birthplace": "Уфа",
            "created_at": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person not found")

@router.put("/persons/{person_id}")
async def update_person(
    person_id: str,
    person: PersonUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Обновляет информацию о персоне"""
    try:
        # TODO: Обновить в Neo4j
        return {
            "status": "success",
            "message": "Person updated"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/persons/{person_id}")
async def delete_person(person_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Удаляет персону из дерева"""
    try:
        # TODO: Удалить из Neo4j
        return {"status": "success", "message": "Person deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/relationships")
async def create_relationship(
    rel: RelationshipCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Создает связь между двумя персонами"""
    try:
        from app.main import graph_engine
        result = await graph_engine.create_relationship(
            rel.person_id_1,
            rel.person_id_2,
            rel.relationship_type
        )
        return {
            "status": "success",
            "relationship": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tree/{person_id}")
async def get_family_tree(
    person_id: str,
    depth: int = 3,
    direction: str = "both",
    current_user_id: str = Depends(get_current_user_id)
):
    """Получает семейное дерево персоны"""
    try:
        from app.main import graph_engine
        tree = await graph_engine.get_family_tree(
            person_id,
            depth=depth,
            direction=direction
        )
        return {
            "status": "success",
            "tree": tree
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/statistics")
async def get_statistics(current_user_id: str = Depends(get_current_user_id)):
    """Получает статистику генеалогического дерева пользователя"""
    try:
        from app.main import graph_engine
        stats = await graph_engine.get_statistics(current_user_id)
        return {
            "status": "success",
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/merge-duplicates")
async def merge_duplicates(
    main_person_id: str = Body(...),
    duplicate_ids: List[str] = Body(...),
    current_user_id: str = Depends(get_current_user_id)
):
    """Объединяет дубликаты в основную персону"""
    try:
        from app.main import graph_engine
        result = await graph_engine.merge_trees(
            current_user_id,
            main_person_id,
            duplicate_ids
        )
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/export")
async def export_tree(
    format: str = "json",
    current_user_id: str = Depends(get_current_user_id)
):
    """Экспортирует генеалогическое дерево"""
    try:
        # TODO: Реализовать экспорт в JSON, CSV, GEDCOM
        return {
            "status": "success",
            "download_url": "https://api.familyroots.ru/export/tree_123.json"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/import")
async def import_tree(
    file_format: str = "gedcom",
    current_user_id: str = Depends(get_current_user_id)
):
    """Импортирует генеалогическое дерево из файла"""
    try:
        # TODO: Реализовать импорт из GEDCOM, JSON, CSV
        return {
            "status": "success",
            "message": "Tree imported",
            "persons_added": 150
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_current_user_id(token: str) -> str:
    """Вспомогательная функция для получения ID текущего пользователя"""
    # TODO: Реализовать JWT верификацию
    return "user_123"
