from functools import reduce
from typing import List
from .transaction import Transaction

def average_unit_price(transactions: List[Transaction]) -> float:
    if not transactions:
        return 0.0
    prices = map(lambda tx: tx.unit_price, transactions)
    total = reduce(lambda acc, p: acc + p, prices, 0.0)
    return round(total / len(transactions), 2)
