import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/megabank.db")

JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PROD")
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

 # optionnel pour plus de cleanitude
JWT_LEEWAY_SECONDS = int(os.getenv("JWT_LEEWAY_SECONDS", "5"))
JWT_ISS = os.getenv("JWT_ISS", "megabank-api") 
JWT_AUD = os.getenv("JWT_AUD", "megabank-web") 