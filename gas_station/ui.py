from .fuel_pump import FuelPump, InsufficientFuelError
from .history import load_history, save_transaction
from .transaction import Transaction
from .utils import average_unit_price
from .stats import plot_liters_vs_cost

def main_menu(pumps: list[FuelPump]):
    while True:
        print("\n=== Symulator stacji benzynowej ===")
        print("1. Zatankuj")
        print("2. Pokaż historię transakcji")
        print("3. Pokaż średnią cenę paliwa")
        print("4. Pokaż wykres: litry vs koszt")
        print("5. Zakończ")
        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            do_refuel(pumps)
        elif choice == "2":
            show_history()
        elif choice == "3":
            show_average_price()
        elif choice == "4":
            plot_liters_vs_cost()
        elif choice == "5":
            print("Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór.")

def do_refuel(pumps):
    for p in pumps:
        print(p)
    try:
        pid = int(input("Numer dystrybutora: "))
        liters = float(input("Ilość litrów: "))
        price  = float(input("Cena za litr (zł): "))
    except ValueError:
        print("Błędne dane wejściowe.")
        return
    pump = next((p for p in pumps if p.pump_id == pid), None)
    if not pump:
        print("Nie znaleziono dystrybutora.")
        return
    try:
        cost = pump.dispense(liters, price)
    except InsufficientFuelError as e:
        print("Błąd:", e)
        return
    tx = Transaction(pid, pump.fuel_type, liters, price)
    save_transaction(tx)
    print(f"Transakcja zakończona. Koszt: {cost:.2f} zł")

def show_history():
    history = load_history()
    if not history:
        print("Brak zapisanych transakcji.")
        return
    for tx in history:
        print(tx)

def show_average_price():
    avg = average_unit_price(load_history())
    print(f"Średnia cena jednostkowa paliwa: {avg:.2f} zł")
