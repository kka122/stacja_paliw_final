# tests/test_performance.py

import timeit
from gas_station.fuel_pump import FuelPump

def setup_pump():
    return FuelPump(1, "ON", 10000.0)

def test_dispense_performance():
    p = setup_pump()
    # Mierzymy 1000 wywołań p.dispense(1, 5.0)
    duration = timeit.timeit(lambda: p.dispense(1, 5.0), number=1000)
    # Sprawdzamy, że to zajmuje np. mniej niż 0.1s
    assert duration < 0.1, f"dispense() za wolno: {duration:.3f}s"
