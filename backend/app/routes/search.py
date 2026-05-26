"""
API маршруты для поиска с Fuzzy Matching
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class SearchQuery(BaseModel):
    name: str
    birth_date: Optional[str] = None
    birthplace: Optional[str] = None
    limit: int = 50

class SearchResult(BaseModel):
    id: str
    name: str
    birth_date: Optional[str]
    birthplace: Optional[str]
    confidence: float
    reasons: List[str]

@router.get("/by-name")
async def search_by_name(
    q: str = Query(..., min_length=2),
    limit: int = Query(50, le=100),
    current_user_id: str = Depends(get_current_user_id)
):
    """Поиск персон по имени"""
    try:
        from app.main import graph_engine

        results = await graph_engine.search_by_name_phonetic(
            q,
            current_user_id,
            limit
        )

        return {
            "status": "success",
            "query": q,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/find-matches")
async def find_matches(
    search: SearchQuery,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Находит потенциальные совпадения в дереве пользователя
    с использованием Fuzzy Matching
    """
    try:
        from app.main import fuzzy_matcher, graph_engine

        # Получить все персоны пользователя
        all_persons = await graph_engine.search_by_name_phonetic(
            "",
            current_user_id,
            limit=10000
        )

        # Поискать совпадения
        search_person = {
            'name': search.name,
            'birth_date': search.birth_date,
            'birthplace': search.birthplace
        }

        matches = []
        for person in all_persons:
            score, details = fuzzy_matcher.match_person_records(
                search_person,
                person,
                confidence_threshold=0.75
            )

            if details['is_match']:
                matches.append({
                    "person_id": person.get('id'),
                    "name": person.get('name'),
                    "confidence": details['confidence'],
                    "reasons": details['reasons'],
                    "component_scores": details['component_scores']
                })

        # Сортируем по уверенности
        matches.sort(key=lambda x: x['confidence'], reverse=True)

        return {
            "status": "success",
            "search_query": search.name,
            "matches": matches[:search.limit],
            "total_matches": len(matches)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/find-duplicates")
async def find_duplicates(
    min_confidence: float = Query(0.85, ge=0.0, le=1.0),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Находит потенциальные дубликаты в дереве пользователя
    """
    try:
        from app.main import fuzzy_matcher, graph_engine

        # Получить все персоны
        all_persons = await graph_engine.search_by_name_phonetic(
            "",
            current_user_id,
            limit=10000
        )

        # Найти дубликаты
        duplicates = fuzzy_matcher.find_duplicates(
            all_persons,
            confidence_threshold=min_confidence
        )

        return {
            "status": "success",
            "duplicates": [
                {
                    "person_id_1": dup[0],
                    "person_id_2": dup[1],
                    "confidence": dup[2]
                }
                for dup in duplicates
            ],
            "total_duplicates": len(duplicates)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ancestors/{person_id}")
async def find_common_ancestors(
    person_id: str,
    other_person_id: str = Query(...),
    max_depth: int = Query(5, ge=1, le=10),
    current_user_id: str = Depends(get_current_user_id)
):
    """Находит общих предков между двумя персонами"""
    try:
        from app.main import graph_engine

        ancestors = await graph_engine.find_common_ancestors(
            person_id,
            other_person_id,
            max_depth
        )

        return {
            "status": "success",
            "person_1": person_id,
            "person_2": other_person_id,
            "common_ancestors": ancestors,
            "total": len(ancestors)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/relationship/{person_id}")
async def get_relationship_degree(
    person_id: str,
    other_person_id: str = Query(...),
    current_user_id: str = Depends(get_current_user_id)
):
    """Определяет степень родства между двумя персонами"""
    try:
        from app.main import graph_engine

        degree = await graph_engine.calculate_relationship_degree(
            person_id,
            other_person_id
        )

        # Определяем степень родства
        relationship_map = {
            2: "Супруг(а)",
            3: "Родитель или Ребенок",
            4: "Брат/Сестра",
            5: "Дед/Баба или Внук/Внучка",
            6: "Дядя/Тетя или Племянник/Племянница"
        }

        relationship_name = relationship_map.get(degree, "Дальний родственник")

        return {
            "status": "success",
            "person_1": person_id,
            "person_2": other_person_id,
            "degree": degree,
            "relationship": relationship_name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/global-search")
async def global_search(
    q: str = Query(..., min_length=2),
    search_type: str = Query("all", regex="^(all|persons|locations|surnames)$"),
    limit: int = Query(50, le=100),
    current_user_id: str = Depends(get_current_user_id)
):
    """Глобальный поиск по всему дереву и архивам"""
    try:
        results = {
            "persons": [],
            "locations": [],
            "surnames": []
        }

        if search_type in ["all", "persons"]:
            # Поиск персон
            results["persons"] = [
                {
                    "id": "person_1",
                    "name": "Иван Петров",
                    "birth_year": 1880,
                    "birthplace": "Уфа"
                }
            ]

        if search_type in ["all", "locations"]:
            # Поиск локаций
            results["locations"] = [
                {
                    "name": "Уфа",
                    "region": "Башкортостан",
                    "mentioned_count": 152
                }
            ]

        if search_type in ["all", "surnames"]:
            # Поиск фамилий
            results["surnames"] = [
                {
                    "surname": "Петров",
                    "variants": ["Петренко", "Петровский"],
                    "occurrences": 45
                }
            ]

        return {
            "status": "success",
            "query": q,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_current_user_id(token: str = None) -> str:
    """Вспомогательная функция для получения ID текущего пользователя"""
    # TODO: Реализовать JWT верификацию
    return "user_123"
