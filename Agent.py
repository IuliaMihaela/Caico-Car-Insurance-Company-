import uuid

# Represents the insurance agent

class Agent:
    def __init__(self, name, address):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.address = address
        self.customers = []
        self.payments = []
        self.claims = []

    def reviewClaim(self, customer, claim):
        if customer in self.customers:  # if the agent has that client
            self.claims.append(claim)  # the claim of the customer is added to the list

    def receivePayment(self, payment):
        self.payments.append(payment)  # the payment received is added to the list

    #convert object o JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'address': self.address
        }
