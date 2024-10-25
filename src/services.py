import json
import logging
import re

from typing import List, Dict
from src.conf import BASE_DIR
from src.utils import reader_transactions_excel

OPERATIONS_DIR = BASE_DIR.joinpath("data", "operations.xlsx")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    filename="../logs/services.log",
    filemode="w",
    encoding="UTF8")

logger = logging.getLogger("services")

def get_transactions_people(dict_transactions: List[Dict], pattern):
    """Функция, которая выбирает переводы физлицам и возвращает JSON"""
    logger.info("Вызвана функция get_transactions_people")
    list_transactions = []
    for trans in dict_transactions:
        if "Описание" in trans and re.match(pattern, trans["Описание"]):
            list_transactions.append(trans)
    logger.info(f"Найдено {len(list_transactions)} транзакций, соответствующих паттерну")
    if list_transactions:
        list_transactions_json = json.dumps(list_transactions, ensure_ascii=False)
        logger.info(f"Возвращен список JSON со {len(list_transactions)} транзакциями")
        return list_transactions_json
    else:
        logger.info(f"Возвращен пустой список")
        return "[]"
