# tests/test_memory.py

import json
import pytest
from pathlib import Path
from memory_profiler import memory_usage

from gas_station.fuel_pump import FuelPump
from gas_station.history import load_history, save_transaction
from gas_station.transaction import Transaction

@pytest.fixture(autouse=True)
def tmp_history(monkeypatch, tmp_path):
    fake = tmp_path / "history.json"
    fake.write_text("[]", encoding="utf-8")
    monkeypatch.setattr('gas_station.history.HISTORY_FILE', fake)
    return fake

def test_dispense_memory_usage():
    p = FuelPump(1, "ON", 10000.0)
    # Mierzymy zużycie pamięci przy 1000 wywołaniach dispense()
    mem_diff = max(memory_usage((lambda: [p.dispense(1, 5.0) for _ in range(1000)]),
                                interval=0.01)) - min(memory_usage((lambda: [p.dispense(1, 5.0) for _ in range(1000)]),
                                                                 interval=0.01))
    # Ustal swój próg – np. nie więcej niż 5 MB narostu
    assert mem_diff < 5, f"Za duże zużycie pamięci: {mem_diff:.2f} MiB"

def test_history_load_save_memory_usage(tmp_history):
    # Przygotuj kilka transakcji
    sample = [Transaction(1, "ON", i, 5.0) for i in range(100)]
    for tx in sample:
        save_transaction(tx)

    # Mierzymy memory_usage dla load_history
    mem = memory_usage((load_history, ), interval=0.01, timeout=1)
    # Sprawdzamy, że nie narasta powyżej 10 MB
    assert max(mem) - min(mem) < 10, f"Za duże zużycie pamięci przy load_history: {max(mem)-min(mem):.2f} MiB"
