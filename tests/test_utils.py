from unittest.mock import patch

import datetime
import datetime as dt

import pandas as pd
import pytest

from src.utils import get_greetings, get_date, reader_transactions_excel


def test_get_greetings_morning():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 8, 0, 0)
            assert get_greetings() == "Доброе утро"


def test_get_greetings_afternoon():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 14, 0, 0)
            assert get_greetings() == "Добрый день"


def test_get_greetings_evening():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 19, 0, 0)
            assert get_greetings() == "Добрый вечер"


def test_get_greetings_night():
    with pytest.raises(TypeError):
        with patch("datetime.datetime.now") as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 1, 0, 0)
            assert get_greetings() == "Доброй ночи"


def test_get_date_input():
    """Проверка корректности ввода даты"""
    input_date = "01.01.2020 13:00:00"
    expected_output = datetime.datetime(2020, 1, 1, 13, 0, 0)
    assert get_date(input_date) == expected_output


def test_get_date_format():
    """Тест на неверный формат"""
    input_date = "01-01-2020 13:00:00"
    with pytest.raises(ValueError):
        get_date(input_date)


def test_get_date_empty():
    """Тест на пустой ввод"""
    input_date = ""
    with pytest.raises(ValueError):
        get_date(input_date)


def test_reader_transactions_excel():
    """Тест на несуществующий файл"""
    with pytest.raises(FileNotFoundError):
        reader_transactions_excel("..\\data\\transactions.xlsx")


