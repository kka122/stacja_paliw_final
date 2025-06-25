# tests/test_integration.py

import json
import pytest
from pathlib import Path

from gas_station.fuel_pump import FuelPump
import gas_station.history as history_mod
from gas_station.history import load_history, save_transaction
from gas_station.transaction import Transaction
from gas_station.utils import average_unit_price
from gas_station.stats import plot_liters_vs_cost
from gas_station.class_diagram import generate_class_diagram

@pytest.fixture(autouse=True)
def tmp_env(monkeypatch, tmp_path):
    # Podmieniamy plik historii na tymczasowy
    fake_hist = tmp_path / "history.json"
    fake_hist.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(history_mod, "HISTORY_FILE", fake_hist)
    # Tworzymy folder docs w tmp_path
    docs = tmp_path / "docs"
    docs.mkdir()
    # Podmieniamy ścieżki zapisu wykresu i diagramu na folder docs
    monkeypatch.setattr('gas_station.stats.OUTPUT_PNG', docs / "liters_over_time.png")
    monkeypatch.setattr('gas_station.class_diagram.OUTPUT_PNG', str(docs / "class_diagram.png"))
    return fake_hist, docs

def test_transaction_and_average(tmp_env):
    """Integracja: tworzymy transakcje, zapisujemy, ładujemy i liczymy średnią."""
    fake_hist, _ = tmp_env

    # 1) Symulujemy dwie transakcje
    t1 = Transaction(1, "ON", 10.0, 5.0)
    save_transaction(t1)
    t2 = Transaction(2, "PB95", 20.0, 6.0)
    save_transaction(t2)

    # 2) Ładujemy historię i sprawdzamy średnią
    hist = load_history()
    assert len(hist) == 2
    expected_avg = (5.0 + 6.0) / 2
    assert average_unit_price(hist) == pytest.approx(expected_avg)

def test_plot_and_diagram_creation(tmp_env):
    """Integracja: wywołanie funkcji generujących wykres i diagram."""
    fake_hist, docs = tmp_env

    # Dodajemy przykładowe transakcje ręcznie do pliku historii
    sample = [
        {"timestamp":"2025-06-25T10:00:00","pump_id":1,"fuel_type":"ON","liters":5.0,"unit_price":5.0,"total_cost":25.0},
        {"timestamp":"2025-06-25T11:00:00","pump_id":2,"fuel_type":"PB95","liters":15.0,"unit_price":6.0,"total_cost":90.0},
    ]
    fake_hist.write_text(json.dumps(sample), encoding="utf-8")

    # 1) Generujemy wykres liniowy litrów w czasie
    plot_liters_vs_cost()
    assert (docs / "liters_over_time.png").exists()

    # 2) Generujemy diagram UML klas
    generate_class_diagram()
    assert (docs / "class_diagram.png").exists()
