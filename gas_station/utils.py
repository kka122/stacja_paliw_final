from functools import reduce
from typing import List
from .transaction import Transaction

def average_unit_price(transactions: List[Transaction]) -> float:
    """
    Zwraca średnią cenę jednostkową paliwa na podstawie listy transakcji.
    """
    if not transactions:
        return 0.0
    prices = map(lambda tx: tx.unit_price, transactions)
    total = reduce(lambda acc, p: acc + p, prices, 0.0)
    return round(total / len(transactions), 2)

def filter_expensive(transactions: List[Transaction], min_cost: float) -> List[Transaction]:
    """
    Zwraca listę transakcji, których koszt całkowity >= min_cost.
    """
    return list(filter(lambda tx: tx.total_cost >= min_cost, transactions))
