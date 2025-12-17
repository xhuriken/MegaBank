from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    uuid: str
    email: EmailStr
    first_name: str
    last_name: str

class Token(BaseModel):
    """
    This represents an auth token payload.
    We use it as the response model for /auth/login.
    """
    access_token: str
    token_type: str = "bearer"

class AuthResponse(BaseModel):
    """
    This wraps a newly created user plus the token.
    We use it as the response model for /auth/register.
    """
    message: str
    user: UserPublic
    access_token: str
    token_type: str = "bearer"