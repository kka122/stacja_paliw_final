import json
from pathlib import Path
from typing import List
from .transaction import Transaction

HISTORY_FILE = Path(__file__).parent.parent / "data" / "history.json"

def load_history() -> List[Transaction]:
    if not HISTORY_FILE.exists():
        return []
    items = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return [Transaction.from_dict(d) for d in items]

def save_transaction(tx: Transaction):
    history = load_history()
    history.append(tx)
    HISTORY_FILE.write_text(
        json.dumps([t.to_dict() for t in history], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
