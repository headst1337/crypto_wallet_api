from typing import Any
from fastapi import APIRouter

from account.utils import generate_mnemonic_seed
from account.account import Account

from account.schemas import (
    Lang,
    MnemonicLenght,
    BaseResponce,
    DataRequest,
    BalanceRequest
)

from account.constants import (
    VALIDATION_ERROR,
    VALIDATION_ERROR_MESSAGE
)

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


@router.get("/create", response_model=BaseResponce)
def create_new_wallet(lang: Lang, mnemonic_length: MnemonicLenght):
    seed, mnemonic = generate_mnemonic_seed(lang, int(mnemonic_length))
    wallet_data = Account.get_wallet_data(seed)
    return {'status': 200, 'response': {'menmonic': mnemonic, 'data': wallet_data}}

@router.post("/data", response_model=BaseResponce)
def get_wallet_data(request: DataRequest):
    if (request.mnemonic is not None):
        seed, mnemonic = generate_mnemonic_seed(mnemonic=request.mnemonic)
        wallet_data = Account.get_wallet_data(seed)
    elif request.private_key is not None:
        wallet_data = Account.get_wallet_data(private_key=request.private_key)
    else: 
        return {
            'status': 400, 
            'error': {'type': VALIDATION_ERROR, 'message': VALIDATION_ERROR_MESSAGE}
        }
    return {'status': 200, 'response': {'data': wallet_data}}

@router.post("/balance", response_model=BaseResponce)
def get_balance(request: BalanceRequest):
    if request.contract_address:
        balance = Account.get_token_balance(request.rpc, request.address, request.contract_address)
    else:
        balance = Account.get_balance(request.rpc, request.address)
    return {'status': 200, 'response' : {'data': balance}}
