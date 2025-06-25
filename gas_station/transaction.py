from datetime import datetime

class Transaction:
    def __init__(self, pump_id: int, fuel_type: str, liters: float, unit_price: float):
        self.timestamp = datetime.now()
        self.pump_id = pump_id
        self.fuel_type = fuel_type
        self.liters = liters
        self.unit_price = unit_price
        self.total_cost = round(liters * unit_price, 2)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "pump_id": self.pump_id,
            "fuel_type": self.fuel_type,
            "liters": self.liters,
            "unit_price": self.unit_price,
            "total_cost": self.total_cost
        }

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        tx = Transaction(
            pump_id=data["pump_id"],
            fuel_type=data["fuel_type"],
            liters=data["liters"],
            unit_price=data["unit_price"]
        )
        tx.timestamp = datetime.fromisoformat(data["timestamp"])
        return tx

    def __repr__(self):
        return (f"<Transaction {self.timestamp:%Y-%m-%d %H:%M:%S} "
                f"dystrybutor={self.pump_id} {self.liters}l @ {self.unit_price}zł = {self.total_cost}zł>")
