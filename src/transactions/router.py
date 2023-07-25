from typing import Any
from fastapi import APIRouter

from transactions.transaction import Transaction

from transactions.schemas import (
    BaseResponce,
    TransactionRequest
)

router = APIRouter(
    prefix="/transaction",
    tags=["Transactions"]
)


@router.post("/send", response_model=BaseResponce)
def send_transaction(request: TransactionRequest):
    if request.contract_address:
        transaction_data = Transaction.send_token_transaction(
            request.rpc, 
            request.address_to, 
            request.amount, 
            request.private_key, 
            request.contract_address
        )
    else :
        transaction_data = Transaction.send_transaction(
            request.rpc, 
            request.address_to, 
            request.amount, 
            request.private_key, 
        )
    return {'status': 200, 'response' : {'data': transaction_data}}

@router.get("/receipt", response_model=BaseResponce)
def get_transaction_receipt(rpc: str, transaction_hash: str):
    transaction_receipt = Transaction.get_transaction_receipt(rpc, transaction_hash)
    return {'status': 200, 'response' : {'data': transaction_receipt}}