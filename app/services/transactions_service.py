"""Service de transacciones con lógica de negocio."""

from app.repositories.transactions_repo import (
    MerchantsRepository,
    TransactionsRepository,
)


class TransactionsService:
    """Service para crear transacciones con validaciones de negocio."""

    @staticmethod
    def create_transaction(merchant_id: str, amount_usd: float) -> dict:
        """
        Crea una transacción validando que el comerciante existe y no está suspendido.

        Args:
            merchant_id: ID del comerciante
            amount_usd: Monto en USD

        Returns:
            Dict con status, transaction_id y message

        Raises:
            ValueError: Si el comerciante está suspendido
        """
        # Validar que el comerciante existe (esta validación ya está en Pydantic)
        merchant = MerchantsRepository.get_merchant(merchant_id)
        if not merchant:
            raise ValueError(f"Comerciante no encontrado: {merchant_id}")

        # Validar que no está suspendido (regla de negocio)
        if MerchantsRepository.is_merchant_suspended(merchant_id):
            raise ValueError("Comerciante suspendido")

        # Generar ID de transacción
        transaction_id = TransactionsRepository.next_transaction_id()

        return {
            "status": "approved",
            "transaction_id": transaction_id,
            "message": f"Transacción aprobada para {merchant.get('name', merchant_id)} ({merchant_id})",
        }
