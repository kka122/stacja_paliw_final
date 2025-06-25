import pytest
from gas_station.fuel_pump import FuelPump, InsufficientFuelError

def test_dispense_and_refill():
    p = FuelPump(1, "ON", 100.0)
    assert p.level == 100.0
    cost = p.dispense(10, 5.0)
    assert cost == 50.0
    assert p.level == 90.0

    with pytest.raises(InsufficientFuelError):
        p.dispense(200, 5.0)

    p.refill(15)
    assert p.level == 100.0  # nie przekracza pojemności

def test_invalid_values():
    p = FuelPump(2, "PB95", 50.0)
    with pytest.raises(ValueError):
        p.dispense(0, 4.0)
    with pytest.raises(ValueError):
        p.refill(0)
