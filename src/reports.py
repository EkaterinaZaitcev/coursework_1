import datetime
import datetime as dt
import logging


import data
import pandas as pd

from src.conf import BASE_DIR
from src.utils import get_date, reader_transactions_excel

OPERATIONS_DIR = BASE_DIR.joinpath("data", "operations.xlsx")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    filename="../logs/reports.log",
    filemode="w",
    encoding="UTF8")

logger = logging.getLogger("reports")


def get_spending_by_category(df_transactions:pd.DataFrame, category:str, date:[str]=None) -> pd.DataFrame:
    """Функция возвращает траты по категориям за последние 3 месяца"""
    logger.info(f"Вызвана функция get_spending_by_category")
    if date is None:
        end_date = dt.datetime.now()
    else:
        end_date = get_date(date)
    start_date = end_date.replace(hour=0, minute=0, second=0)-datetime.timedelta(days=91)
    transactions_by_category = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)<=end_date)
        &(pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)>=start_date)
    &(df_transactions["Категория"]==category)
    ]
    return transactions_by_category


if __name__ =="__main__":
    result = get_spending_by_category(reader_transactions_excel(OPERATIONS_DIR),
                                      "Аптеки", "19.11.2021 18:35:32")
    print(result)
