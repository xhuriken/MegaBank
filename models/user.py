from sqlmodel import SQLModel, Field
from ..core.identifiers import new_uuid

class User(SQLModel, table=True):
    uuid: str = Field(default_factory=new_uuid, primary_key=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    first_name: str
    last_name: str
