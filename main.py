from fastapi import FastAPI
from .db.database import init_db
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.accounts import router as accounts_router
from .routes.deposits import router as deposits_router
from .routes.withdrawals import router as withdrawals_router
from .routes.transactions import router as transactions_router

app = FastAPI(title="MegaBank")

# Enregistre les routes
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(deposits_router)
app.include_router(withdrawals_router)
app.include_router(transactions_router)

@app.on_event("startup")
def on_startup():
    init_db()
