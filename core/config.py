import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./megabank.db")
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PROD")
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
