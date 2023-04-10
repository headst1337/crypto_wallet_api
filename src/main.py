from fastapi import FastAPI

from account.router import router as router_account

app = FastAPI(
    title="Crypto Wallet API"
)

app.include_router(router_account)