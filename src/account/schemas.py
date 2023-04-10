from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, validator


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
    status : int
    response: Optional[Any]

class GetDataRequest(BaseModel):
    mnemonic: Optional[list]
    private_key: Optional[str] = Field(max_length=64)
