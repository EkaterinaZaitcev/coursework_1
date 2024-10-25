import datetime
import logging
from src.conf import BASE_DIR

OPERATIONS_DIR = BASE_DIR.joinpath("data", "operations.xlsx")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    filename="../logs/utils.log",
    filemode="w",
    encoding="UTF8")

logger = logging.getLogger("utils")

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
