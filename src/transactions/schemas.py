from typing import Any, Optional
from pydantic import BaseModel, Field


class BaseResponce(BaseModel):
    status: int = 200
    response: Optional[Any]

class TransactionRequest(BaseModel):
    rpc: str
    address_to: str = Field(max_length=42)
    amount: float
    private_key: str = Field(max_length=64)
    contract_address: Optional[str] = Field(None, max_length=42)