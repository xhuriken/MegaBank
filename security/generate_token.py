import datetime
from ..models.user import User

import jwt

secret_key = "j'aime le caca"
algorithm = "HS256"

def generate_token(user: User):
    payload = {
        "userId": user.id,
    }

    #        "exp": datetime.utcnow() + datetime.timedelta(hours=24),

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token