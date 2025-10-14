class Account():
    iban: str
    balance: float
    isPrimay: bool
    userId: int

    def __init__(self, iban, balance, isPrimay, userId):
        self.iban = iban
        self.balance = balance
        self.isPrimay = isPrimay
        self.userId = userId

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount need to be > 0")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount need to be > 0")
        if self.balance < amount:
            raise ValueError("Not enought bonk")
        self.balance -= amount

