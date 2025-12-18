import uuid
import random
import string

def new_uuid() -> str:
    return str(uuid.uuid4())

#TODO: l'adapter pour une nat en param, et toujours mettre 69420 en premier serie de chiffre.
def generate_iban() -> str:
    country = "FR"
    check = f"{random.randint(0, 9)}{random.randint(0, 9)}"
    rest = "".join(random.choices(string.ascii_uppercase + string.digits, k=24))
    return f"{country}{check}{rest}"
