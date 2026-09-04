from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float = Field(gt=0, description="Amount must be strictly positive")
    currency: CurrencyEnum
    timestamp: datetime

    @field_validator("amount")
    @classmethod
    def validate_max_limit(cls, value: float) -> float:
        # Regulatory threshold check (reject single transfers > 100k)
        if value > 100_000.0:
            raise ValueError("Transaction exceeds single-transfer regulatory limit")
        return round(value, 2)