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


class User():
    id: int
    firstName: str
    lastName: str
    email: str
    password: str

    def __init__(self, id, firstName, lastName, email,password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

class TransactionHistory():
    date: str
    amount: int
    senderIban: str
    receiverIban: str

    def __init__(self,date,amount, senderIban, receiverIban):
        self.date = date
        self.amount = amount
        self.senderIban = senderIban
        self.receiverIban = receiverIban
    
    def __str__(self):
        return {self.date,self,self.amount,self.senderIban,self.receiverIban}

class Beneficiary():
    name: str
    iban: str
    userid: int

    def __init__(self, name: str, iban: str, userid: int):
        self.name = name
        self.iban = iban
        self.userid = userid