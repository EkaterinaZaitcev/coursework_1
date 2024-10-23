import json

from src.utils import get_greetings, get_card_expenses, transactions_currency, get_currency_rates, get_stock_price, \
    top_transactions


def main(df_transactions, date, user_currencies):
    """Главная функция, делающая вывод на главную страницу"""
    greeting = get_greetings()
    transaction = transactions_currency(df_transactions, date)
    cards = get_card_expenses(df_transactions)
    top_trans = top_transactions(df_transactions)
    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_price()

    date_json = json.dumps(
        {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_trans,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )
    return date_json
