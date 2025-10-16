from datetime import datetime, timedelta
from ..models.user import User

import jwt

secret_key = "j'aime le caca"
algorithm = "HS256"

def generate_token(user: User):

    expire_at = datetime.now() + timedelta(days=1)
    now = datetime.utcnow()

    payload = {
        "id": user.id,
        "iat": int(now.timestamp()),
        "exp": int(expire_at.timestamp())
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token