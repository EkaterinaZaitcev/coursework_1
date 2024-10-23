from importlib.resources import path
from locale import currency
from pathlib import Path
from src.conf import BASE_DIR
from src.utils import reader_transactions_excel
from src.views import main


OPERATIONS_DIR = BASE_DIR.joinpath("data", "operations.xlsx")


if __name__ == "__main__":
    df_transactions = reader_transactions_excel(OPERATIONS_DIR)
    date = "29.07.2019 22:06:27"
    currency="USD"
    date_json = main(df_transactions, date, currency)

    print(date_json)
    #print(Path)

