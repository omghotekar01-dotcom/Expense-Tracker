from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    id: Optional[int]
    date: str  # ISO date
    amount: float
    category: str
    type: str  # 'expense' or 'income'
    notes: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class RecurringRule:
    id: Optional[int]
    transaction_id: int
    interval: str  # 'monthly' etc
    next_date: str
