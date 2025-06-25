#!/usr/bin/env python3
"""Punkt wejścia aplikacji i generowanie diagramu po zakończeniu."""
from gas_station.fuel_pump import FuelPump
from gas_station.ui import main_menu
from gas_station.class_diagram import generate_class_diagram

def load_config():
    """Ładuje konfigurację dystrybutorów (można później z JSON)."""
    return [
        FuelPump(1, "ON", 500.0),
        FuelPump(2, "PB95", 300.0),
        FuelPump(3, "LPG", 200.0),
    ]

def main():
    pumps = load_config()
    main_menu(pumps)
    # po zakończeniu – diagram UML
    try:
        generate_class_diagram()
    except Exception as e:
        print("⚠️ Błąd generowania diagramu:", e)

if __name__ == "__main__":
    main()
