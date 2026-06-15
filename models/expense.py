from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    id: int
    date: str
    amount: float
    category: str
    source: str
    raw_text: Optional[str] = None