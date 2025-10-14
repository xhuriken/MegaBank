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
