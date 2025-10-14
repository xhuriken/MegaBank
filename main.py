from fastapi import FastAPI
from .routes import account_routes, user_routes, transfer_routes, beneficiary_routes

app = FastAPI(title="Mega Bank !")

app.include_router(account_routes.router)
app.include_router(user_routes.router)
app.include_router(transfer_routes.router)
app.include_router(beneficiary_routes.router)


@app.get("/")
def root():
    return {"message": "Bienvenue sur FastAPI!"}