from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, validator


class Lang(str, Enum):
    ru = 'ru'
    en = 'en'

class MnemonicLenght(str, Enum):
    L12 = '12'
    L24 = '24'

class BaseResponce(BaseModel):
    status: int = 200
    response: Optional[Any]

class DataRequest(BaseModel):
    mnemonic: Optional[str] = None
    private_key: Optional[str] = Field(None, max_length=64) 

    @validator('mnemonic', 'private_key', pre=True, always=True)
    def check_mnemonic_or_private_key(cls, v, values):
        if v is None and values.get('private_key') is None:
            raise ValueError("At least one of 'mnemonic' or 'private_key' must be provided.")
        return v

class BalanceRequest(BaseModel):
    rpc: str	
    address: str = Field(max_length=42)
    contract_address: Optional[str] = Field(None, max_length=42)
