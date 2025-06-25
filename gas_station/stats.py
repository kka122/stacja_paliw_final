#!/usr/bin/env python3
"""
Moduł statystyk: generuje wykres liniowy ilości zatankowanego paliwa w kolejnych transakcjach.
"""
import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

HISTORY_FILE = Path(__file__).parent.parent / "data" / "history.json"
OUTPUT_PNG   = Path(__file__).parent.parent / "docs" / "liters_over_time.png"

def plot_liters_vs_cost():  # zachowujemy nazwę dla kompatybilności z UI
    """
    Rysuje wykres liniowy: ilość litrów w kolejnych transakcjach w czasie.
    """
    if not HISTORY_FILE.exists():
        print(f"Brak pliku historii: {HISTORY_FILE}")
        return

    data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    if not data:
        print("Brak transakcji do wyświetlenia.")
        return

    # Sortujemy transakcje wg czasu
    data_sorted = sorted(data, key=lambda tx: tx["timestamp"])
    dates = [datetime.fromisoformat(tx["timestamp"]) for tx in data_sorted]
    liters = [tx["liters"] for tx in data_sorted]

    plt.figure(figsize=(8, 6))
    plt.plot(dates, liters, marker='o', linestyle='-')
    plt.title('Ilość zatankowanego paliwa w kolejnych transakcjach')
    plt.xlabel('Czas transakcji')
    plt.ylabel('Ilość litrów [l]')
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PNG)
    print(f"🔄 Wykres zapisany: {OUTPUT_PNG}")
    plt.show()