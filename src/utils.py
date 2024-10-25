import datetime
import datetime as dt
import json
import logging
import os

from typing import Dict, List
from pathlib import Path
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


def reader_transactions_excel(path:str|Path) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает DataFrame"""
    logger.info(f"Вызвана функция reader_transactions_excel с файлом {path}")
    try:
        df_transactions = pd.read_excel(path)
        logger.info(f"Функция {path} найден, данные прочитаны")
        return df_transactions
    except FileNotFoundError:
        logger.info(f"Файл {path} не найден")
        raise


def get_dict_transactions(path) -> List[Dict]:
    """Функция преобразует DataFrame в словарь Python"""
    logger.info(f"Вызвана функция get_dict_transactions с файлом {path}")
    try:
        df = pd.read_excel(path)
        logger.info(f"Файл {path} прочитан")
        df = df.fillna('')
        dict_transactions = df.to_dict('records')
        logger.info(f"Файл {path} преобразован")
        return dict_transactions
    except FileNotFoundError:
        logger.error(f"Файл {path} не найден")
        raise


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


def get_currency_rates(currencies):
    """Функция показывает курсы валют"""
    logger.info("Вызвана функция get_currency_rates")
    to='RUB'
    amount = 1
    API_KEY = os.environ.get("API_KEY")
    url = f"https://api.apilayer.com/currency_data/convert?to={to}&from={currencies}&amount={amount}"
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос отклонен.{status_code}")
    else:

        result = response.json()
        return result


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


def get_card_expenses(df_transactions):
    """Функция возвращает расходы по картам"""
    logger.info("Вызвана функция get_card_expenses")
    card_dict = (df_transactions.loc[df_transactions["Сумма платежа"]<0]
                 .groupby(by='Номер карты').agg("Сумма платежа").sum().to_dict())
    logger.debug("Возвращен словарь расходов по картам")
    card_expenses = []
    for card, expenses in card_dict.items():
        card_expenses.append(
            {"last_digits":card[-4:], "total_spent":abs(expenses), "cashback":abs(round(expenses/100,2))}
        )
        logging.info("Завершение выполнения функции")
        return card_expenses


def top_transactions(df_transactions):
    """Функция, выводит топ-5 транзакций по сумме платежа"""
    logging.info("Начало работы функции top_transactions")
    top_transaction = df_transactions.sort_values(by="Сумма платежа", ascending=True).iloc[:5]
    logger.info("Получен топ 5 транзакций по сумме платежа")
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                "date": str(
                    (datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S"))
                    .date()
                    .strftime("%d.%m.%Y")
                ).replace("-", "."),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logger.info("Сформирован список топ 5 транзакций")
    return top_transaction_list
