import datetime

def get_date(date: str) -> datetime.datetime:
    """Функция преобразования даты"""
    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        return date
    except ValueError as i:
        raise f'Ошибка даты {i}'


def reader_transactions_excel(file_path) -> :
    """Функция принимает на вход путь до файла и возвращает JSON-ответ"""

