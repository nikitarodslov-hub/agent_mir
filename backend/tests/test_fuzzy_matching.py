"""
Тесты для алгоритма Fuzzy Matching
"""

import pytest
from app.services.fuzzy_matching import FuzzyMatcher

@pytest.fixture
def matcher():
    return FuzzyMatcher()

def test_normalize_name(matcher):
    """Тест нормализации имен"""
    assert matcher.normalize_name("ИВАН") == "иван"
    assert matcher.normalize_name("  Петр  ") == "петр"
    assert matcher.normalize_name("Фон Штерн") == "штерн"

def test_name_similarity(matcher):
    """Тест сходства имен"""
    # Точное совпадение
    score = matcher.calculate_name_similarity("Иван", "Иван")
    assert score > 0.9

    # Частичное совпадение
    score = matcher.calculate_name_similarity("Иван", "Иванов")
    assert 0.7 < score < 0.95

    # Совпадение с ошибкой
    score = matcher.calculate_name_similarity("Иван", "Иван")
    assert score > 0.8

def test_transliteration(matcher):
    """Тест исторической транслитерации"""
    variants = matcher.transliterate_historical("король")
    assert len(variants) > 0
    assert "король" in variants

def test_date_comparison(matcher):
    """Тест сравнения дат"""
    # Точное совпадение
    score = matcher._compare_dates("1880-01-15", "1880-01-15")
    assert score == 1.0

    # Дата в пределах допуска (2 года)
    score = matcher._compare_dates("1880-01-15", "1881-01-15")
    assert 0.7 < score < 1.0

    # Дата вне допуска
    score = matcher._compare_dates("1880-01-15", "1885-01-15")
    assert score == 0.0

def test_location_comparison(matcher):
    """Тест сравнения мест"""
    # Точное совпадение
    score = matcher._compare_locations("Уфа", "Уфа")
    assert score == 1.0

    # Исторические варианты
    score = matcher._compare_locations("Уфа", "Уфимск")
    assert score > 0.7

def test_social_class_comparison(matcher):
    """Тест сравнения сословий"""
    # Точное совпадение
    score = matcher._compare_social_class("Дворянин", "Дворянин")
    assert score == 1.0

    # Похожие сословия
    score = matcher._compare_social_class("Купец", "Торговец")
    assert score > 0.5

def test_match_person_records(matcher):
    """Тест сопоставления записей о персонах"""
    person1 = {
        'name': 'Иван Петрович',
        'birth_date': '1880-01-15',
        'birthplace': 'Уфа',
        'social_class': 'Дворянин'
    }

    person2 = {
        'name': 'Иван Петров',
        'birth_date': '1880-01-20',
        'birthplace': 'Уфа',
        'social_class': 'Дворянин'
    }

    score, details = matcher.match_person_records(person1, person2)

    assert score > 0.8
    assert details['is_match'] == True
    assert details['confidence'] > 80

def test_find_duplicates(matcher):
    """Тест поиска дубликатов"""
    persons = [
        {
            'id': '1',
            'name': 'Иван Петрович',
            'birth_date': '1880-01-15',
            'birthplace': 'Уфа'
        },
        {
            'id': '2',
            'name': 'Иван Петров',
            'birth_date': '1880-01-15',
            'birthplace': 'Уфа'
        },
        {
            'id': '3',
            'name': 'Петр Иванович',
            'birth_date': '1850-05-20',
            'birthplace': 'Казань'
        }
    ]

    duplicates = matcher.find_duplicates(persons, confidence_threshold=0.85)

    assert len(duplicates) > 0
    # Первые две должны совпадать
    assert any(d[0] == '1' and d[1] == '2' for d in duplicates)
