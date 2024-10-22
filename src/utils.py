import datetime
import datetime as dt
import logging
import os
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

from src.conf import BASE_DIR

load_dotenv("..\\.env")
OPERATIONS_DIR = BASE_DIR.joinpath("data", "operations.xlsx")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    filename="../logs/utils.log",
    filemode="w",
    encoding="UTF8")

logger = logging.getLogger("utils")


def get_greetings():
    """Функция приветствия пользователя"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


"""if __name__ == "__main__":
    print(get_greetings())"""


def get_date(data: str) -> datetime.datetime:
    """Функция преобразования даты"""
    logger.info(f"Получена строка: {data}")
    try:
        data = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Преобразована в объект: {data}")
        return data
    except ValueError as i:
        logger.error(f"Ошибка преобразования даты: {i}")
        raise i


"""if __name__ == "__main__":
    print(get_date("19.10.2024 14:41:12"))"""


def reader_transactions_excel(file_path:str) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает DataFrame"""
    logger.info(f"Вызвана функция reader_transactions_excel с файлом {file_path}")
    try:
        df_transactions = pd.read_excel(file_path)
        logger.info(f"Функция {file_path} найден, данные прочитаны")
        return df_transactions
    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        raise


"""if __name__ == "__main__":
    print(reader_transactions_excel(OPERATIONS_DIR))"""


def get_dict_transactions(file_path) -> List[Dict]:
    """Функция преобразует DataFrame в словарь Python"""
    logger.info(f"Вызвана функция get_dict_transactions с файлом {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} прочитан")
        df = df.fillna('')
        dict_transactions = df.to_dict('records')
        logger.info(f"Файл {file_path} преобразован")
        return dict_transactions
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        raise


"""if __name__ == "__main__":
    print(get_dict_transactions(OPERATIONS_DIR))"""


def transactions_currency(df_transactions, data) -> pd.DataFrame:
    """Функция сортирующая расходы в интервале времени"""
    end_data = get_date(data)
    start_data = end_data.replace(day=1)
    end_data = end_data.replace(hour=0, minute=0, second=0) + dt.timedelta(days = 1)
    transaction_currency = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= end_data)
        & (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) >= start_data)
    ]
    return transaction_currency


"""if __name__ == "__main__":
    transactions_currency = transactions_currency(reader_transactions_excel(OPERATIONS_DIR), "20.05.2020 11:26:33")
    print(transactions_currency)"""


def get_currency_rates():
    """Функция показывает курсы валют"""
    logger.info("Вызвана функция get_currency_rates")
    API_KEY = os.environ.get("API_KEY")
    url = f"https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=USD,EUR"
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос отклонен.{status_code}")
    else:
        result = response.json()
        return result


"""if __name__ == "__main__":
    currency_rates = get_currency_rates()
    print(currency_rates)"""


def get_stock_price():
    """Функция показывает курс акций"""
    logger.info("Вызвана функция get_currency_rates")
    access_key = os.environ.get("access_key")
    url = f"http://api.marketstack.com/v1/eod?access_key={access_key}&symbols=AAPL,NVDA,MSFT,GOOG,AMZN"
    headers = {"apikey": access_key}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос отклонен.{status_code}")
    else:
        result = response.json()
        return result


"""if __name__ == "__main__":
    stock_price = get_stock_price()
    print(stock_price)"""
