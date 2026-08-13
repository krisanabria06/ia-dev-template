from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TransactionOut(BaseModel):
    transaction_id: str
    merchant_id: str
    amount_usd: float
    timestamp: datetime
    status: str
    pan_masked: Optional[str] = None


class TransactionsPage(BaseModel):
    items: List[TransactionOut]
    next_cursor: Optional[str] = None
