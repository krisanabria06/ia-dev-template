"""Repository in-memory para transacciones y comerciantes."""


class MerchantsRepository:
    """Repository de comerciantes con datos fake in-memory."""

    # Datos de ejemplo fijos
    _merchants = {
        "MCHT-00001": {
            "merchant_id": "MCHT-00001",
            "name": "Farmacia Central Santiago",
            "status": "active",
        },
        "MCHT-00002": {
            "merchant_id": "MCHT-00002",
            "name": "Restaurante El Parrón",
            "status": "active",
        },
        "MCHT-00003": {
            "merchant_id": "MCHT-00003",
            "name": "TechStore Providencia",
            "status": "active",
        },
        "MCHT-00042": {
            "merchant_id": "MCHT-00042",
            "name": "Importadora Rápida Ltda.",
            "status": "active",
        },
        "MCHT-00099": {
            "merchant_id": "MCHT-00099",
            "name": "Outlet Moda Sur",
            "status": "suspended",
        },
    }

    @classmethod
    def get_merchant(cls, merchant_id: str) -> dict | None:
        """Obtiene un comerciante por ID. Retorna None si no existe."""
        return cls._merchants.get(merchant_id)

    @classmethod
    def merchant_exists(cls, merchant_id: str) -> bool:
        """Verifica si un comerciante existe."""
        return merchant_id in cls._merchants

    @classmethod
    def is_merchant_suspended(cls, merchant_id: str) -> bool:
        """Verifica si un comerciante está suspendido."""
        merchant = cls._merchants.get(merchant_id)
        return merchant is not None and merchant.get("status") == "suspended"


class TransactionsRepository:
    """Repository de transacciones con contador para generar IDs."""

    _transaction_counter = 0

    @classmethod
    def next_transaction_id(cls) -> str:
        """Genera el siguiente ID de transacción (determinístico para tests)."""
        cls._transaction_counter += 1
        return f"TXN-2026-{cls._transaction_counter:06d}"

    @classmethod
    def reset(cls) -> None:
        """Reinicia el contador (útil para tests)."""
        cls._transaction_counter = 0
