"""
Graph Engine - вычислительное ядро на базе Neo4j
Отвечает за хранение и анализ генеалогических связей
"""

from neo4j import GraphDatabase, Session
from typing import List, Dict, Optional, Tuple
import asyncio
from datetime import datetime
import uuid

class GraphEngine:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def _run_query(self, query: str, parameters: Dict = None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    async def create_person(
        self,
        user_id: str,
        name: str,
        birth_date: Optional[str] = None,
        death_date: Optional[str] = None,
        birthplace: Optional[str] = None,
        gender: str = "U"
    ) -> Dict:
        """Создает новую персону в графе"""
        person_id = str(uuid.uuid4())
        query = """
        CREATE (p:Person {
            id: $person_id,
            user_id: $user_id,
            name: $name,
            birth_date: $birth_date,
            death_date: $death_date,
            birthplace: $birthplace,
            gender: $gender,
            created_at: datetime()
        })
        RETURN p
        """
        result = self._run_query(query, {
            'person_id': person_id,
            'user_id': user_id,
            'name': name,
            'birth_date': birth_date,
            'death_date': death_date,
            'birthplace': birthplace,
            'gender': gender
        })
        return {"id": person_id, "name": name, "status": "created"}

    async def create_relationship(
        self,
        person_id_1: str,
        person_id_2: str,
        relationship_type: str
    ) -> Dict:
        """
        Создает связь между двумя персонами
        Types: PARENT_OF, SPOUSE_OF, SIBLING_OF, CHILD_OF
        """
        query = f"""
        MATCH (p1:Person {{id: $p1}}), (p2:Person {{id: $p2}})
        CREATE (p1)-[rel:{relationship_type} {{created_at: datetime()}}]->(p2)
        RETURN rel
        """
        result = self._run_query(query, {
            'p1': person_id_1,
            'p2': person_id_2
        })
        return {"relationship": relationship_type, "status": "created"}

    async def find_common_ancestors(
        self,
        person_id_1: str,
        person_id_2: str,
        max_depth: int = 5
    ) -> List[Dict]:
        """Находит общих предков между двумя персонами до заданной глубины"""
        query = f"""
        MATCH (p1:Person {{id: $p1}})-[:PARENT_OF*..{max_depth}]->(ancestor),
              (p2:Person {{id: $p2}})-[:PARENT_OF*..{max_depth}]->(ancestor)
        RETURN DISTINCT ancestor
        LIMIT 100
        """
        result = self._run_query(query, {
            'p1': person_id_1,
            'p2': person_id_2
        })
        return result

    async def get_family_tree(
        self,
        person_id: str,
        depth: int = 3,
        direction: str = "both"  # both, up, down
    ) -> Dict:
        """Получает семейное дерево персоны с указанной глубиной"""
        if direction == "up":
            query = f"""
            MATCH (root:Person {{id: $person_id}})
            MATCH path = (root)-[:PARENT_OF*..{depth}]->(ancestor)
            RETURN root, collect(DISTINCT ancestor) as ancestors
            """
        elif direction == "down":
            query = f"""
            MATCH (root:Person {{id: $person_id}})
            MATCH path = (ancestor)-[:PARENT_OF*..{depth}]->(root)
            RETURN root, collect(DISTINCT ancestor) as descendants
            """
        else:
            query = f"""
            MATCH (root:Person {{id: $person_id}})
            MATCH ancestors_path = (ancestor)-[:PARENT_OF*..{depth}]->(root)
            MATCH descendants_path = (root)-[:PARENT_OF*..{depth}]->(descendant)
            RETURN root,
                   collect(DISTINCT ancestor) as ancestors,
                   collect(DISTINCT descendant) as descendants
            """

        result = self._run_query(query, {'person_id': person_id})
        return result[0] if result else {}

    async def search_by_name_phonetic(
        self,
        name: str,
        user_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Поиск персон по имени с фонетическим учетом"""
        # Это базовый поиск, реальный Fuzzy Matching происходит в отдельном сервисе
        query = """
        MATCH (p:Person {user_id: $user_id})
        WHERE p.name CONTAINS $name
        RETURN p
        LIMIT $limit
        """
        result = self._run_query(query, {
            'user_id': user_id,
            'name': name,
            'limit': limit
        })
        return result

    async def calculate_relationship_degree(
        self,
        person_id_1: str,
        person_id_2: str
    ) -> Optional[int]:
        """Вычисляет степень родства между двумя персонами"""
        query = """
        MATCH path = shortestPath(
            (p1:Person {id: $p1})-[*..10]-(p2:Person {id: $p2})
        )
        RETURN length(path) as degree
        """
        result = self._run_query(query, {
            'p1': person_id_1,
            'p2': person_id_2
        })
        return result[0]['degree'] if result else None

    async def get_statistics(self, user_id: str) -> Dict:
        """Получает статистику по генеалогическому дереву пользователя"""
        query = """
        MATCH (p:Person {user_id: $user_id})
        WITH COUNT(p) as total_persons
        MATCH (p1:Person {user_id: $user_id})-[rel]->(p2:Person {user_id: $user_id})
        WITH total_persons, COUNT(rel) as total_relationships,
             COUNT(DISTINCT p1) as persons_with_relationships
        RETURN total_persons, total_relationships, persons_with_relationships
        """
        result = self._run_query(query, {'user_id': user_id})
        if result:
            return result[0]
        return {"total_persons": 0, "total_relationships": 0}

    async def merge_trees(self, user_id: str, main_person_id: str, duplicate_ids: List[str]) -> Dict:
        """Объединяет дубликаты персон в основную персону"""
        for dup_id in duplicate_ids:
            query = """
            MATCH (dup:Person {id: $dup_id})-[rel]->(other)
            MATCH (main:Person {id: $main_id})
            CREATE (main)-[new_rel:MERGED_RELATION]->(other)
            DELETE rel, dup
            """
            self._run_query(query, {
                'dup_id': dup_id,
                'main_id': main_person_id
            })
        return {"status": "merged", "duplicates_merged": len(duplicate_ids)}
