from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TransactionOut(BaseModel):
    transaction_id: str
    merchant_id: str
    amount_usd: float
    timestamp: datetime
    status: str
    pan_masked: str | None = None


class TransactionsPage(BaseModel):
    items: list[TransactionOut]
    next_cursor: str | None = None
