"""Router para transacciones."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.transactions import TransactionCreate, TransactionResponse
from app.services.transactions_service import TransactionsService

router = APIRouter(tags=["Transacciones"])


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(payload: TransactionCreate) -> TransactionResponse:
    """
    Crea una nueva transacción.

    Valida que el comerciante exista (Pydantic) y no esté suspendido (Service).

    - 201: Transacción aprobada
    - 403: Comerciante suspendido
    - 422: Validación Pydantic fallida
    """
    try:
        result = TransactionsService.create_transaction(
            merchant_id=payload.merchant_id,
            amount_usd=payload.amount_usd,
        )
        return TransactionResponse(**result)
    except ValueError as e:
        if "suspendido" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Comerciante suspendido",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
