from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    """Schema de entrada para crear una transacción."""

    merchant_id: str = Field(
        ...,
        pattern=r"^MCHT-\d{5}$",
        description="ID de comerciante en formato MCHT-XXXXX",
    )
    amount_usd: float = Field(..., gt=0, description="Monto en USD, debe ser positivo")


class TransactionResponse(BaseModel):
    """Schema de respuesta cuando se crea una transacción."""

    status: str
    transaction_id: str
    message: str
