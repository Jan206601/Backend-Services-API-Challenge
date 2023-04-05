"""

Backend Services & API Challenge
Simple consumer loan application

Author: Jan Ulrich Sütt

"""
import datetime

from flask import Flask, jsonify, request

from database_access import DAO
from loan_application import LoanApplication

app = Flask(__name__)
database = DAO()

MAX_APPLICATIONS_PER_DAY = 5
INTEREST_RATE = 0.05


@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    # Read data from POST body
    data = request.get_json()
    loan_amount = data['loan_amount']
    loan_term = data['loan_term']
    name = data['name']
    personal_id = data['personal_id']
    current_date = datetime.date.today().strftime("%d.%m.%Y")

    # Create LoanApplication instance
    loan_application = LoanApplication(
        loan_amount=loan_amount,
        loan_term=loan_term,
        application_date=current_date,
        interest_rate=INTEREST_RATE,
        name=name,
        personal_id=personal_id
    )

    # Check if person is in blacklist
    if database.person_in_blacklist(personal_id):
        return jsonify({'status': 'rejected', 'message': 'Person is blacklisted!'}, 400)

    # Check if person has done too many applications
    person_apps = database.get_loan_applications(personal_id)
    person_apps_today = [loan_app for loan_app in person_apps if loan_app.application_date == current_date]
    if len(person_apps_today) > MAX_APPLICATIONS_PER_DAY:
        return jsonify({'status': 'rejected', 'message': 'Too many applications in a day!'}, 400)

    # Add loan application to database
    database.add_loan_application(loan_application)
    return jsonify({'status': 'accepted', 'data': loan_application.serialize()}), 201


@app.route('/loans/<string:personal_id>', methods=['GET'])
def get_loans(personal_id):
    # Get all loan applications for given personal_id
    loan_applications = database.get_loan_applications(personal_id)
    loans_serialized = [loan_application.serialize() for loan_application in loan_applications]
    return jsonify({'personal_id': personal_id, 'loans': loans_serialized})


if __name__ == '__main__':
    app.run(port=50000)
