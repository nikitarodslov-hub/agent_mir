"""
Fuzzy Matching - алгоритм вероятностного сопоставления генеалогических данных
Учитывает фонетические искажения, историческую транслитерацию и региональные специфики
"""

from fuzzywuzzy import fuzz, process
from typing import List, Tuple, Dict, Optional
from datetime import datetime
import re
import json

class FuzzyMatcher:
    def __init__(self):
        # Исторические правила транслитерации для Урала и Поволжья
        self.transliteration_rules = {
            'й': 'i',
            'ё': 'e',
            'ы': 'y',
            'э': 'e',
            'ц': 'c',
            'х': 'h',
            'ш': 'sh',
            'щ': 'sch',
            'ж': 'zh',
            'ч': 'ch'
        }

        # Татарские и башкирские имена с частыми искажениями
        self.ethnicity_patterns = {
            'tatar': ['хали', 'фатима', 'мария', 'гаврила', 'габдула', 'дина'],
            'bashkir': ['раиса', 'эльза', 'булат', 'азат', 'разия'],
            'russian': ['иван', 'мария', 'петр', 'анна', 'дмитрий']
        }

        # Сословия Российской империи
        self.social_classes = {
            'дворянин': 'nobility',
            'купец': 'merchant',
            'крестьянин': 'peasant',
            'мещанин': 'townspeople',
            'однодворец': 'odnodvorets',
            'казак': 'cossack',
            'тептярь': 'teptyar',
            'припущенник': 'pripu­shchennik'
        }

    def normalize_name(self, name: str) -> str:
        """Нормализует имя для сравнения"""
        if not name:
            return ""

        name = name.lower().strip()

        # Удаляем приставки и суффиксы
        prefixes = ['де ', 'фон ', 'ван ', 'ле ']
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]

        # Заменяем ё на е
        name = name.replace('ё', 'е')

        return name

    def transliterate_historical(self, text: str) -> List[str]:
        """Генерирует варианты исторической транслитерации"""
        variants = [text.lower()]

        for cyrillic, latin in self.transliteration_rules.items():
            variant = text.lower().replace(cyrillic, latin)
            if variant not in variants:
                variants.append(variant)

        return variants

    def calculate_name_similarity(
        self,
        name1: str,
        name2: str,
        consider_history: bool = True
    ) -> float:
        """Вычисляет схожесть двух имен с учетом исторических искажений"""

        n1 = self.normalize_name(name1)
        n2 = self.normalize_name(name2)

        # Прямое сравнение
        direct_score = fuzz.ratio(n1, n2) / 100.0

        if consider_history:
            # Историческая транслитерация
            variants1 = self.transliterate_historical(n1)
            variants2 = self.transliterate_historical(n2)

            best_score = direct_score
            for v1 in variants1:
                for v2 in variants2:
                    score = fuzz.ratio(v1, v2) / 100.0
                    if score > best_score:
                        best_score = score

            return best_score

        return direct_score

    def match_person_records(
        self,
        person1: Dict,
        person2: Dict,
        confidence_threshold: float = 0.85
    ) -> Tuple[float, Dict]:
        """
        Сопоставляет две записи о персоне
        Возвращает уверенность сопоставления и детали совпадения
        """

        scores = {}
        weights = {}

        # 1. Сравнение имен (вес 40%)
        name_score = self.calculate_name_similarity(
            person1.get('name', ''),
            person2.get('name', '')
        )
        scores['name'] = name_score
        weights['name'] = 0.40

        # 2. Сравнение дат рождения (вес 30%)
        birth_score = self._compare_dates(
            person1.get('birth_date'),
            person2.get('birth_date')
        )
        scores['birth'] = birth_score
        weights['birth'] = 0.30

        # 3. Географическое совпадение (вес 15%)
        location_score = self._compare_locations(
            person1.get('birthplace'),
            person2.get('birthplace')
        )
        scores['location'] = location_score
        weights['location'] = 0.15

        # 4. Сословие и социальный статус (вес 10%)
        class_score = self._compare_social_class(
            person1.get('social_class'),
            person2.get('social_class')
        )
        scores['class'] = class_score
        weights['class'] = 0.05

        # Вычисляем взвешенную оценку
        total_score = sum(scores[k] * weights[k] for k in scores)

        match_details = {
            'total_score': round(total_score, 3),
            'component_scores': {k: round(v, 3) for k, v in scores.items()},
            'is_match': total_score >= confidence_threshold,
            'confidence': round(total_score * 100, 1),
            'reasons': self._generate_match_reasons(scores, person1, person2)
        }

        return total_score, match_details

    def _compare_dates(
        self,
        date1: Optional[str],
        date2: Optional[str],
        tolerance_years: int = 2
    ) -> float:
        """Сравнивает две даты с допуском"""
        if not date1 or not date2:
            return 0.5  # Нейтральная оценка если одна из дат отсутствует

        try:
            d1 = datetime.fromisoformat(date1)
            d2 = datetime.fromisoformat(date2)

            diff = abs((d1 - d2).days)
            tolerance_days = tolerance_years * 365

            if diff == 0:
                return 1.0
            elif diff <= tolerance_days:
                return 1.0 - (diff / tolerance_days) * 0.3
            else:
                return 0.0
        except:
            return 0.5

    def _compare_locations(self, loc1: Optional[str], loc2: Optional[str]) -> float:
        """Сравнивает географические местоположения"""
        if not loc1 or not loc2:
            return 0.5

        loc1 = loc1.lower()
        loc2 = loc2.lower()

        if loc1 == loc2:
            return 1.0

        # Исторические названия мест
        historical_variants = {
            'уфа': ['уфимск', 'уфа'],
            'казань': ['казань', 'казанский'],
            'поволжье': ['волга', 'поволжье']
        }

        for city, variants in historical_variants.items():
            if any(v in loc1 for v in variants) and any(v in loc2 for v in variants):
                return 0.9

        similarity = fuzz.ratio(loc1, loc2) / 100.0
        return similarity

    def _compare_social_class(self, class1: Optional[str], class2: Optional[str]) -> float:
        """Сравнивает социальные сословия"""
        if not class1 or not class2:
            return 0.5

        if class1.lower() == class2.lower():
            return 1.0

        # Близкие сословия
        similar_classes = {
            'дворянин': ['помещик', 'барин'],
            'купец': ['торговец', 'негоциант'],
            'крестьянин': ['пахарь', 'селянин'],
            'мещанин': ['бещик', 'посадский']
        }

        for main_class, variants in similar_classes.items():
            if (class1.lower() == main_class or class1.lower() in variants) and \
               (class2.lower() == main_class or class2.lower() in variants):
                return 0.7

        return 0.0

    def _generate_match_reasons(
        self,
        scores: Dict[str, float],
        person1: Dict,
        person2: Dict
    ) -> List[str]:
        """Генерирует пояснения для сопоставления"""
        reasons = []

        if scores['name'] > 0.9:
            reasons.append("Имена совпадают")
        elif scores['name'] > 0.7:
            reasons.append("Имена похожи (возможное историческое искажение)")

        if scores['birth'] > 0.9:
            reasons.append("Даты рождения совпадают")
        elif scores['birth'] > 0.5:
            reasons.append("Даты рождения близки")

        if scores['location'] > 0.8:
            reasons.append("Место рождения совпадает")
        elif scores['location'] > 0.5:
            reasons.append("Место рождения в одном регионе")

        return reasons

    def find_duplicates(
        self,
        persons: List[Dict],
        confidence_threshold: float = 0.85
    ) -> List[Tuple[str, str, float]]:
        """Находит потенциальные дубликаты в списке персон"""
        duplicates = []

        for i, person1 in enumerate(persons):
            for j, person2 in enumerate(persons[i+1:], start=i+1):
                score, _ = self.match_person_records(
                    person1,
                    person2,
                    confidence_threshold
                )

                if score >= confidence_threshold:
                    duplicates.append((
                        person1.get('id'),
                        person2.get('id'),
                        score
                    ))

        return duplicates
