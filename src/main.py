from fastapi import FastAPI

from account.router import router as router_account
from transactions.router import router as router_transaction

app = FastAPI(
    title="Crypto Wallet API"
)

app.include_router(router_account)
app.include_router(router_transaction)