from datetime import datetime
import pytest
from pydantic import ValidationError
from src.consumer import evaluate_transaction
from src.models import CurrencyEnum, Transaction


def test_valid_transaction_settles():
    payload = {
        "transaction_id": "tx-100",
        "user_id": "usr-88",
        "amount": 250.50,
        "currency": "EUR",
        "timestamp": datetime.utcnow().isoformat(),
    }
    tx = Transaction(**payload)
    status = evaluate_transaction(tx)
    assert status == "SETTLED"


def test_high_value_transaction_flagged_for_review():
    payload = {
        "transaction_id": "tx-101",
        "user_id": "usr-88",
        "amount": 15000.00,
        "currency": "GBP",
        "timestamp": datetime.utcnow().isoformat(),
    }
    tx = Transaction(**payload)
    status = evaluate_transaction(tx)
    assert status == "FLAGGED_REVIEW"


def test_negative_amount_fails_validation():
    payload = {
        "transaction_id": "tx-102",
        "user_id": "usr-88",
        "amount": -10.00,
        "currency": "USD",
        "timestamp": datetime.utcnow().isoformat(),
    }
    with pytest.raises(ValidationError):
        Transaction(**payload)


def test_exceeding_regulatory_limit_fails():
    payload = {
        "transaction_id": "tx-103",
        "user_id": "usr-88",
        "amount": 150000.00,
        "currency": "EUR",
        "timestamp": datetime.utcnow().isoformat(),
    }
    with pytest.raises(ValidationError):
        Transaction(**payload)