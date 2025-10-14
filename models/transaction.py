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
