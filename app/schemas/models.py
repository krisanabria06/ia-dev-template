from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    merchant_id: str = Field(pattern=r"^MCHT-\d{5}$")
    amount_usd: float = Field(gt=0)


class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
