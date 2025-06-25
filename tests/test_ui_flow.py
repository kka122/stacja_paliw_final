import json
import pytest
from pathlib import Path
from gas_station.fuel_pump import FuelPump
from gas_station.ui import main_menu
import gas_station.history as history_mod

@pytest.fixture(autouse=True)
def temp_history_file(monkeypatch, tmp_path):
    # Podstawiamy pusty plik historii
    fake = tmp_path / "history.json"
    fake.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(history_mod, "HISTORY_FILE", fake)
    return fake

def test_full_refuel_and_history_flow(monkeypatch, capsys, temp_history_file):
    pumps = [FuelPump(1, "ON", 100.0), FuelPump(2, "PB95", 50.0)]
    # symulujemy kolejne wpisy użytkownika:
    # 1 – tankuj, pompa 1, 10l po 5zł; 2 – pokaż historię; 5 – zakończ
    inputs = iter(["1","1","10","5","2","5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main_menu(pumps)
    out = capsys.readouterr().out

    # sprawdzamy, że program poinformował o zakończeniu transakcji
    assert "Transakcja zakończona. Koszt: 50.00 zł" in out
    # sprawdzamy, że w historii pojawiła się odpowiednia transakcja
    assert "<Transaction" in out and "dystrybutor=1" in out
    # i że w pliku JSON rzeczywiście zapisał się jeden rekord
    data = json.loads(temp_history_file.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["pump_id"] == 1 and data[0]["liters"] == 10

def test_insufficient_fuel_path(monkeypatch, capsys, temp_history_file):
    pumps = [FuelPump(1, "ON", 5.0)]
    # próbujemy zatankować 10l przy dostępnych 5l
    inputs = iter(["1","1","10","4","5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main_menu(pumps)
    out = capsys.readouterr().out

    # powinien pokazać błąd i nie zapisać nic do historii
    assert "Błąd: Brak paliwa" in out
    assert json.loads(temp_history_file.read_text(encoding="utf-8")) == []
