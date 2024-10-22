import pytest
import json
from src.services import get_transactions_people



def test_get_transactions_people(dict_transactions):
    """Тест проверки операций физлицам"""
    pattern = r"Константин Л."
    result = get_transactions_people(dict_transactions, pattern)
    expected = json.dumps([
        {"Описание": "Константин Л."},
        ],
        ensure_ascii=False,
    )
    assert result == expected