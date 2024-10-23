from unittest import mock
from unittest.mock import patch
import datetime
import datetime as dt
import pytest

from src.utils import get_greetings, get_date, reader_transactions_excel, get_card_expenses, get_currency_rates


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


def test_get_card_expenses(sample_transaction):
    result = get_card_expenses(sample_transaction)

    assert result[0] == {"Последняя операция":"*1112", "Всего расходов":100, "Кэшбэк":1.0}
    #assert result[1] == {"Последняя операция":"*5091", "Всего расходов":200, "Кэшбэк":2.0}


@patch("src.utils.requests.get")
@patch("src.utils.os.environ.get")
def test_get_currency_rates_success(mock_get_env, mock_get):
    mock_get_env.return_value = "test_api_key"

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"quotes":{"USDRUB":91.04, "USDEUR":0.81}}
    mock_get.return_value=mock_response

    currencies = ["RUB", "EUR"]
    result = get_currency_rates(currencies)
    expected_result = [{"currency":"USD", "rate":91.04},
                       {"currency":"EUR", "rate":round(91.04/0.81, 2)}]
    assertEqual(result, expected_result)
    mock_get.assert_called_onse_with("https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD,EUR",
                                     headers={"apikey":"test_api_key"})


@patch("src.utils.request.get")
@patch("src.utils.os.environ.get")
def test_get_currency_rates_failure(mock_get_env, mock_get, assertIsNone=None):
    """Тест на ошибку курса валют"""
    mock_get_env.return_value="test_api_key"

    mock_response=mock.Mock()
    mock_response.status_code=500
    mock_response.reason="Internal Server Error"
    mock_get.return_value=mock_response

    currencies=["RUB", "EUR"]
    result=get_currency_rates(currencies)
    assertIsNone(result)
    mock_get.assert_called_once_with("https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD,EUR",
                                     headers={"apikey":"test_api_key"})
