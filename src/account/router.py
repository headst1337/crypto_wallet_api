from fastapi import APIRouter

from account.utils import generate_mnemonic_seed
from account.account import Account

from account.schemas import (
    Lang,
    MnemonicLenght,
    BaseResponce,
    GetDataRequest,
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
def get_wallet_data(request: GetDataRequest):
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
