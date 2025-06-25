import pytest
from gas_station.transaction import Transaction
from datetime import datetime

def test_to_from_dict():
    tx = Transaction(1, "ON", 10.0, 5.5)
    d = tx.to_dict()
    assert d["pump_id"] == 1
    assert d["fuel_type"] == "ON"
    assert d["liters"] == 10.0
    assert d["unit_price"] == 5.5
    assert "timestamp" in d

    tx2 = Transaction.from_dict(d)
    assert tx2.pump_id == tx.pump_id
    assert tx2.fuel_type == tx.fuel_type
    assert tx2.liters == tx.liters
    assert tx2.unit_price == tx.unit_price
    assert isinstance(tx2.timestamp, datetime)
