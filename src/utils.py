import datetime
import pandas as pd
from typing import List, Dict


def get_greetings(hour):
    """Функция приветствия пользователя"""
    hour = dt.datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12<= hour <17:
        return "Добрый день"
    elif 17<= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

if __name__ == "__main__":
    print(get_greetings("14:25"))

def get_date(date: str) -> datetime.datetime:
    """Функция преобразования даты"""
    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        return date
    except ValueError as i:
        raise f'Ошибка даты {i}'


def reader_transactions_excel(file_path) -> List[Dict]:
    """Функция принимает на вход путь до файла и возвращает словарь python"""
    try:
        df = pd.read_excel(file_path)
        dict_transactions = df.to_dict(orient = "records")
        return dict_transactions
    except FileNotFoundError:
        raise f'Ошибка, файл не найден'


