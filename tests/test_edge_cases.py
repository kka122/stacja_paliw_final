import pytest
import json
from pathlib import Path
from gas_station.fuel_pump import FuelPump, InsufficientFuelError
from gas_station.transaction import Transaction
import gas_station.history as history_mod
from gas_station.history import load_history, save_transaction

@pytest.fixture(autouse=True)
def tmp_history(monkeypatch, tmp_path):
    # Tymczasowy plik historii
    fake = tmp_path / "history.json"
    fake.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(history_mod, "HISTORY_FILE", fake)
    return fake

# --- Testy FuelPump dla wartości brzegowych i błędnych ---

def test_dispense_zero_liters_raises():
    p = FuelPump(1, "ON", 50.0)
    with pytest.raises(ValueError):
        p.dispense(0, 5.0)

def test_dispense_negative_liters_raises():
    p = FuelPump(1, "ON", 50.0)
    with pytest.raises(ValueError):
        p.dispense(-1, 5.0)

def test_refill_zero_raises():
    p = FuelPump(1, "ON", 50.0)
    with pytest.raises(ValueError):
        p.refill(0)

def test_refill_negative_raises():
    p = FuelPump(1, "ON", 50.0)
    with pytest.raises(ValueError):
        p.refill(-10)

def test_capacity_assertion():
    with pytest.raises(AssertionError):
        FuelPump(1, "ON", 0)   # capacity musi być > 0

# --- Testy Transaction dla nietypowych wartości ---

def test_transaction_negative_liters_and_price():
    tx = Transaction(1, "ON", -5.0, -4.0)
    assert tx.liters == -5.0
    assert tx.unit_price == -4.0
    # total_cost = (-5.0) * (-4.0) = 20.0
    assert tx.total_cost == pytest.approx(20.0)

# --- Testy historii z niepoprawnym plikiem JSON ---

def test_load_history_non_json(tmp_history):
    tmp_history.write_text("NOT A JSON", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_history()

def test_load_history_empty_file(tmp_path, monkeypatch):
    fake = tmp_path / "history.json"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(history_mod, "HISTORY_FILE", fake)
    with pytest.raises(json.JSONDecodeError):
        load_history()

def test_save_transaction_creates_valid_structure(tmp_history):
    tx = Transaction(1, "PB95", 10.0, 4.5)
    save_transaction(tx)
    data = json.loads(tmp_history.read_text(encoding="utf-8"))
    # Sprawdzamy, że klucz “total_cost” i inne są obecne
    assert all(k in data[0] for k in ["timestamp", "pump_id", "fuel_type", "liters", "unit_price", "total_cost"])
