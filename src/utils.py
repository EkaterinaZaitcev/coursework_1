import datetime

from typing import List, Dict

import pandas as pd

def get_greetings():
    """Функция приветствия пользователя"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12<= hour <17:
        return "Добрый день"
    elif 17<= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

"""if __name__ == "__main__":
    print(get_greetings("12:00"))"""

def get_date(date: str) -> datetime.datetime:
    """Функция преобразования даты"""
    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        return date
    except ValueError as i:
        raise f'Ошибка даты {i}'

"""if __name__ == "__main__":
    print(get_date("19.10.2024 14:41:12"))"""

def reader_transactions_excel(file_path:str) -> List[Dict]:
    """Функция принимает на вход путь до файла и возвращает словарь python"""
    with open(file_path, 'r', encoding='utf-8'):
        reader = pd.read_excel(file_path)
        reader = reader.fillna('0')
        header = pd.DataFrame(reader, columns=["transaction_date", "payment_date",
                    "card_number", "status", "amount", "currency", "payment_amount",
                    "payment_currency", "cashback", "category", "mcc", "description",
                    "bonuses", "investment_piggy", "amount_with_rounding"])
        dict_transactions = header.to_dict('records')
        return dict_transactions

"""if __name__ == "__main__":
    print(reader_transactions_excel("..\\data\\operations.xlsx"))"""
