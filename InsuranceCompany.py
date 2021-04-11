from Customer import *
from Agent import *
import random


class InsuranceCompany:
    def __init__(self, name):
        self.name = name  # Name of the Insurance company
        self.customers = []  # list of customers
        self.agents = []  # list of dealers
        self.claims = []  # list of claims
        self.payments_in = []  # list of payments from customers
        self.payments_out = []  # list of payments to agents

    def transferCustomers(self, agent_id):
        agent = self.getAgentById(agent_id)  # get the agent object
        new_agent = random.choice([a for a in self.agents if a != agent])  # randomly select an agent different from the one we want to delete
        new_agent.customers = new_agent.customers + agent.customers  # append the customers of the deleted agent to the list of customers of the new one
        new_agent.claims = new_agent.claims + agent.claims  # add also the claims from the deleted agent

    def AssignAgentForCustomer(self, agent, customer):
        agent.customers.append(customer)  # append the customer to the list of customers of the given agent

    #for payments
    def addPaymentIn(self, paymentIn):
        self.payments_in.append(paymentIn)  # append the payment made by a customer to the list
        return paymentIn.ID

    def addPaymentOut(self, paymentOut):
        self.payments_out.append(paymentOut)  # append the payment transferred to an agent to the list
        return paymentOut.ID

    def getPaymentsIn(self):
        return list(self.payments_in)  # return a list of payments made by customers

    def getPaymentsOut(self):
        return list(self.payments_out)  # return a list of payments transferred to agents

    #for claims
    def getClaimById(self, id_):
        for d in self.claims:
            if d.ID == id_:
                return d
        return None

    def manageClaim(self, claim_id, status):
        c = self.getClaimById(claim_id)  # get the claim object
        if c:
            c.changeStatus(status)
            return True
        return False

    def addClaim(self, claim):
        self.claims.append(claim)
        return claim.ID

    def getClaims(self):
        return list(self.claims)  # return a list of all claims

    #for customers
    def getCustomers(self):
        return list(self.customers)  # return a list of all customers

    def addCustomer(self, name, address):
        c = Customer(name, address)
        self.customers.append(c)  # append the customer to the list of customers
        return c.ID

    def getCustomerById(self, id_):
        for d in self.customers:
            if d.ID == id_:
                return d
        return None

    def deleteCustomer(self, customer_id):
        c = self.getCustomerById(customer_id)
        if c:
            for a in self.agents:
                if c in a.customers:
                    a.customers.remove(c)  # remove customer from its agent's list of customers
            self.customers.remove(c)  # remove customer from the company's list of customers
            return True
        return False

    #for agents
    def getAgents(self):
        return list(self.agents)  # return a list of all agents

    def addAgent(self, name, address):
        a = Agent(name, address)
        self.agents.append(a)  # append agent to the list of agents
        return a.ID

    def getAgentById(self, id_):
        for d in self.agents:
            if d.ID == id_:
                return d
        return None

    def deleteAgent(self, agent_id):
        a = self.getAgentById(agent_id)
        if a:
            self.agents.remove(a)
            return True
        return False

    #statistics
    def displayStatisticsCustomer(self, customer):
        print("The customer,", customer.name, " with id: ", customer.ID, " has respective cars: ", customer.cars, ",claims: ", customer.claims, "and payments made: ", customer.payments)

    def displayBestAgents(self):
        return sorted(self.agents, key=lambda a: len(a.customers)+len(a.claims) + sum([p.amount for p in a.payments]), reverse=True)