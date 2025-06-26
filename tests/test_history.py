import pytest
import json
from pathlib import Path
import gas_station.history as h
from gas_station.transaction import Transaction

@pytest.fixture(autouse=True)
def tmp_history(monkeypatch, tmp_path):
    fake = tmp_path / "history.json"
    fake.write_text("[]", encoding="utf-8")  # Plik nie jest pusty!
    monkeypatch.setattr(h, "HISTORY_FILE", fake)
    return fake

def test_save_and_load(tmp_history):
    tx = Transaction(1, "ON", 5.0, 4.5)
    h.save_transaction(tx)
    hist = h.load_history()
    assert len(hist) == 1
    assert hist[0].pump_id == 1
    assert hist[0].total_cost == tx.total_cost
