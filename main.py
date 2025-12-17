from fastapi import FastAPI
from db.database import init_db
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.accounts import router as accounts_router
from routes.deposits import router as deposits_router
from routes.withdrawals import router as withdrawals_router
from routes.transactions import router as transactions_router
from routes.beneficiaries import router as beneficiaries_router
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="MegaBank")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# This middleware handles CORS and preflight OPTIONS requests.
# Without it, your POST from React never reaches the /auth/register route.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Only these origins are allowed to call your API
    allow_credentials=True,       # Needed if you later use cookies / auth headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers like Content-Type, Authorization
)

# Enregistre les routes

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(deposits_router)
app.include_router(withdrawals_router)
app.include_router(transactions_router)
app.include_router(beneficiaries_router)

@app.on_event("startup")
def on_startup():
    init_db()
