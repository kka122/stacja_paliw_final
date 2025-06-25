class InsufficientFuelError(Exception):
    """Wyjątek rzucany, gdy nie ma wystarczająco paliwa na dystrybutorze."""
    pass

class FuelPump:
    def __init__(self, pump_id: int, fuel_type: str, capacity: float):
        assert capacity > 0, "Pojemność musi być dodatnia"
        self.pump_id = pump_id
        self.fuel_type = fuel_type
        self.capacity = capacity       # maksymalna ilość litrów
        self.level = capacity          # obecny stan paliwa (start pełen)

    def dispense(self, liters: float, unit_price: float) -> float:
        """Wydaje określoną liczbę litrów, zwraca koszt.
        Rzuca InsufficientFuelError, jeśli level < liters."""
        if liters <= 0:
            raise ValueError("Ilość litrów musi być większa od zera")
        if self.level < liters:
            raise InsufficientFuelError(f"Brak paliwa: dostępne {self.level}l, wymagane {liters}l")
        self.level -= liters
        return round(liters * unit_price, 2)

    def refill(self, amount: float):
        """Uzupełnia stan paliwa o podaną ilość, nie przekraczając capacity."""
        if amount <= 0:
            raise ValueError("Ilość uzupełnienia musi być dodatnia")
        self.level = min(self.capacity, self.level + amount)

    def __repr__(self):
        return (f"<FuelPump id={self.pump_id} typ={self.fuel_type} "
                f"pojemność={self.capacity}l, stan={self.level}l>")
