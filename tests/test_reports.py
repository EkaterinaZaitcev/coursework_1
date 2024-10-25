from src.reports import get_spending_by_category


def test_spending_by_category_with_date(operation_data):
    """Тест функции с указанной датой и категорией"""
    result = get_spending_by_category(operation_data, "Супермаркет", "19.11.2021 18:54:29")
    assert (len(result) == 3)
