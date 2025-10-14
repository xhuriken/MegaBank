class Beneficiary():
    name: str
    iban: str
    userid: int

    def __init__(self, name: str, iban: str, userid: int):
        self.name = name
        self.iban = iban
        self.userid = userid