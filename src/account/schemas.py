from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class Lang(str, Enum):
    ru = 'ru'
    en = 'en'

class MnemonicLenght(str, Enum):
    L12 = '12'
    L13 = '13'
    L15 = '15'
    L18 = '18'
    L21 = '21'
    L24 = '24'
    L25 = '25'

class BaseResponce(BaseModel):
    status : int = 200
    response: Optional[Any]

class GetDataRequest(BaseModel):
    mnemonic: Optional[str]
    private_key: Optional[str] = Field(max_length=64)

class GetBalanceRequest(BaseModel):
    rpc: str	
    address : str = Field(max_length=42)
    contract_address : Optional[str] = Field(max_length=42)
