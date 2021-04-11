from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *
from Agent import *

app = Flask(__name__)

# Root object for the insurance company
company = InsuranceCompany("Be-Safe Insurance Company")


# Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")


# Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if (c != None):
        return jsonify(c.serialize())
    return jsonify(
        success=False,
        message="Customer not found")


# Add a new car (parameters: model, numberplate).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if (c != None):
        car = Car(request.args.get('model'), request.args.get('number_plate'), request.args.get('motor_power'))
        c.addCar(car)
        return jsonify("Car added to the customer with id "+str(customer_id))
    return jsonify(
        success=c != None,
        message="Customer not found")

# Delete the customer with the given customer_id.
@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if (result):
        message = f"Customer with id {customer_id} was deleted"
    else:
        message = "Customer not found"
    return jsonify(
        success=result,
        message=message)

#Return a list of all customers
@app.route("/customers", methods=["GET"])
def allCustomers():
    return jsonify(customers=[{"customer": h.serialize(), "cars" : [c.serialize() for c in h.cars]} for h in company.getCustomers()])


# Add a new agent (parameters: name, address).
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    cid = company.addAgent(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new agent with ID {cid}")


# Return the details of a agent of the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def agentInfo(agent_id):
    a = company.getAgentById(agent_id)
    if (a != None):
        return jsonify(a.serialize())
    return jsonify(
        success=False,
        message="Agent not found")


# Assign a new customer with the provided customer_id to the agent with agent_id.
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def AssignAgentForCustomer(agent_id, customer_id):
    a = company.getAgentById(agent_id)
    c = company.getCustomerById(customer_id)
    if (c != None and a != None):  # if both agent's and customer's ids exist
        company.AssignAgentForCustomer(a, c)
        return jsonify(f"Customer with id {customer_id} assigned to agent with id {agent_id}.")
    return jsonify(
        success=c != None,
        message="Customer or Agent not found")

# Delete the agent with the given agent_id.
@app.route("/agent/<agent_id>", methods=["DELETE"])
def deleteAgent(agent_id):
    company.transferCustomers(agent_id)
    result = company.deleteAgent(agent_id)
    if (result):
        message = f"Agent with id {agent_id} was deleted"
    else:
        message = "Agent not found"
    return jsonify(
        success=result,
        message=message)

# Return a list of all agents.
@app.route("/agents", methods=["GET"])
def allAgents():
    return jsonify(agents=[h.serialize() for h in company.getAgents()])


# Add a new insurance claim (parameters: date, incident_description, claim_amount).
@app.route("/claims/<customer_id>/file", methods=["POST"])
def addClaim(customer_id):
    c = company.getCustomerById(customer_id)
    if (c != None):
        claim = InsuranceClaim(request.args.get('date'), request.args.get('incident_description'), request.args.get('claim_amount'))
        c.fileUpClaims(claim)
        claimId=company.addClaim(claim)
        for a in company.agents:  # for every agent in company
            a.reviewClaim(c, claim)  # check if the agent is suitable for reviewing the claim
        return jsonify(f"Added a new claim with id {claimId}")
    return jsonify(
        success=c != None,
        message="Customer not found")


# Return the details of a claim with the the given claim_id.
@app.route("/claims/<claim_id>", methods=["GET"])
def claimInfo(claim_id):
    c = company.getClaimById(claim_id)
    if (c != None):
        return jsonify(c.serialize())
    return jsonify(
        success=False,
        message="Claim not found")

# Change the status of a claim to REJECTED, PARTLY COVERED or FULLY COVERED. Parameters: approved_amount.
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def changeStatus(claim_id):
    result = company.manageClaim(claim_id, request.args.get('approved_amount'))
    if (result):
        message = f"The status with id {claim_id} was changed"
    else:
        message = "Claim not found"
    return jsonify(
        success=result,
        message=message)

# Return a list of all claims.
@app.route("/claims", methods=["GET"])
def allClaims():
    return jsonify(claims=[c.serialize() for c in company.getClaims()])

# Add a new payment received from a customer. (parameters: date, customer_id, amount_received)
@app.route("/payment/in/", methods=["POST"])
def addPaymentIn():
    c = company.getCustomerById(request.args.get('customer_id'))
    if (c != None):
        payment = PaymentIn(request.args.get('date'), c, request.args.get('amount_received'))
        c.makePayment(payment)
        paymentId=company.addPaymentIn(payment)
        return jsonify(f"Added a new payment with id {paymentId} received from customer with id {c.ID}.")
    return jsonify(
        success=c != None,
        message="Customer not found")

# Add a new payment transferred to an agent. (parameters: date, agent_id, amount_sent).
@app.route("/payment/out/", methods=["POST"])
def addPaymentOut():
    a = company.getAgentById(request.args.get('agent_id'))
    if (a != None):
        payment = PaymentOut(request.args.get('date'), a, request.args.get('amount_sent'))
        a.receivePayment(payment)
        paymentId = company.addPaymentOut(payment)
        return jsonify(f"Added a new payment with id {paymentId} transferred to agent with id {a.ID}.")
    return jsonify(
        success=a != None,
        message="Agent not found")

# Return a list of all incoming and outgoing payments.
@app.route("/payments/", methods=["GET"])
def allPayments():
    return jsonify(incoming_payments=[p.serialize() for p in company.getPaymentsIn()], outgoing_payments=[p.serialize() for p in company.getPaymentsOut()])

# Return a list of all claims, grouped by responsible agents
@app.route("/stats/claims", methods=["GET"])
def allClaimsWthAgent():
    return jsonify(claims=[{a.ID: [c.serialize() for c in a.claims]} for a in company.getAgents()])

# Return a list of all revenues, grouped by responsible agents
@app.route("/stats/revenues", methods=["GET"])
def statsRevenues():
    return jsonify(revenues=[{a.ID: [p.serialize() for p in a.payments]} for a in company.getAgents()])

# Return a sorted list of agents based on their performance.
@app.route("/stats/agents", methods=["GET"])
def statsAgents():
    result = company.displayBestAgents()
    return jsonify(agents=[a.serialize() for a in result])





###DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
        success=True,
        message="Your server is running! Welcome to the Insurance Company API.")


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE"
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8888)