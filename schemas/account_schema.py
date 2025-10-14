from pydantic import BaseModel

#c'est les model de con pydantic on verra si ça nous sert (c'est censé nous servrir mais je comprends toujours pas)from pydantic import BaseModel

class DepositRequest(BaseModel):
    amount: float

class WithdrawRequest(BaseModel):
    amount: float
