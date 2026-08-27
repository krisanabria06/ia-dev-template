from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_transaction_happy_path_returns_201() -> None:
    # Arrange
    payload = {
        "merchant_id": "MCHT-00001",
        "amount_usd": 150.0,
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "approved"
    assert body["transaction_id"] == "TXN-2026-000001"
    assert "MCHT-00001" in body["message"]


def test_create_transaction_rejects_invalid_field_with_422() -> None:
    # Arrange
    payload = {
        "merchant_id": "INVALID-ID",
        "amount_usd": 150.0,
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any(error["loc"][-1] == "merchant_id" for error in body["detail"])


def test_create_transaction_borde_case_prd_returns_forbidden_for_suspended_merchant() -> None:
    # Arrange
    payload = {
        "merchant_id": "MCHT-00099",
        "amount_usd": 75.0,
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 403
    body = response.json()
    assert body["detail"] == "Comerciante suspendido"
