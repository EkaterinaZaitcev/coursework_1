import json
import re

from typing import List, Dict

from src.utils import reader_transactions_excel


def get_transactions_people(dict_transactions: List[Dict], pattern):
    """Функция, которая выбирает переводы физлицам и возвращает JSON"""
    list_transactions = []
    for trans in dict_transactions:
        if "description" in trans and re.match(pattern, trans["description"]):
            list_transactions.append(trans)
    if list_transactions:
        list_transactions_json = json.dumps(list_transactions, ensure_ascii=False)
        return list_transactions_json
    else:
        return "[]"

"""if __name__ == "__main__":
    list_transactions_json = get_transactions_people(
        reader_transactions_excel("..\\data\\operations.xlsx"), pattern=r"\b[А-Я][а-я]+\s[А-Я]\."
    )
    print(list_transactions_json)"""