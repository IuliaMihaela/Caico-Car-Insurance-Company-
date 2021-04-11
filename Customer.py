import uuid

# Represents the customer of the car insurance company
class Customer:
    def __init__(self, name, address):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.address = address
        self.cars = []  # List of cars
        self.claims = []  # list of claims
        self.payments = []  # list of payments

    def __repr__(self):
        return self.name+" with ID:"+self.ID

    def addCar(self, car):
        self.cars.append(car)

    def removeCar(self, car):
        self.cars.remove(car)

    def fileUpClaims(self, claim):
        self.claims.append(claim)  # add the new claim to the list

    def makePayment(self, payment):
        self.payments.append(payment)   # add the new payment to the list

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'address': self.address,
        }


class Car:
    def __init__(self, model_name, number_plate, motor_power):
        self.name = model_name
        self.number_plate = number_plate
        self.motor_power = motor_power
        # self.year = ""

    def __repr__(self):
        return self.number_plate+", "+self.model

    def serialize(self):
        return {
            'model_name': self.name,
            'number_plate': self.number_plate,
            'motor_power': self.motor_power,
            # 'year': self.year,
        }

class InsuranceClaim:
    def __init__(self, date, incident_description, amount):
        self.ID = str(uuid.uuid1())
        self.date = date
        self.incident_description = incident_description
        self.amount = amount
        self.status = ""

    def changeStatus(self, status):
        self.status = status

    def serialize(self):
        return {
            'ID': self.ID,
            'date': self.date,
            'incident_description': self.incident_description,
            'amount': self.amount,
            'status': self.status,
        }

class PaymentIn:
    def __init__(self, date, customer, amount):
        self.date = date
        self.amount = amount
        self.customer = customer
        self.ID = str(uuid.uuid1())

    def serialize(self):
        return {
            'ID': self.ID,
            'date': self.date,
            'customer': self.customer.ID,
            'amount': self.amount,
        }


class PaymentOut:
    def __init__(self, date, agent, amount):
        self.date = date
        self.amount = amount
        self.agent = agent
        self.ID = str(uuid.uuid1())

    def serialize(self):
        return {
            'ID': self.ID,
            'date': self.date,
            'agent': self.agent.ID,
            'amount': self.amount,
        }