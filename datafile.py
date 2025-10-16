from .models.account import *
from .models.user import *
from .models.beneficiary import *

users = {

}

accounts = {
}

beneficiaries = {
    1: Beneficiary(name="Alice Amie", iban="FR 18974", userid=1),
    2: Beneficiary(name="Mon Compte Épargne", iban="FR 032523", userid=1),
    3: Beneficiary(name="Bob Collègue", iban="FR 2352", userid=2)
}

Transactions = []
typeUserActual = None


