from .models.account import *
from .models.user import *
from .models.beneficiary import *

users = {
    1 : User(1, "Jean", "1", "email","gyuezgef"),
    2 : User(2, "Fabrice", "2", "email","giugyyig"),
    3 : User(3, "test", "test", "email","huihuh"),
}

accounts = {
    "FR 0" : Account("FR 020", 10,  True, 1),
    "FR 1" : Account("FR 102", 100, False, 1),
    "FR 2" : Account("FR 223", 30,  True, 2),
    "FR 3" : Account("FR 223", 30,  True, 3),
}

beneficiaries = {
    1: Beneficiary(name="Alice Amie", iban="FR 18974", userid=1),
    2: Beneficiary(name="Mon Compte Épargne", iban="FR 032523", userid=1),
    3: Beneficiary(name="Bob Collègue", iban="FR 2352", userid=2)
}

Transactions = []
typeUserActual = None


