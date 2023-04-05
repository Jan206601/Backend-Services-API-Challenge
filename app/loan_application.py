
class LoanApplication:
    def __init__(self, loan_amount, loan_term, application_date: str, interest_rate, name, personal_id):
        self.loan_amount = loan_amount
        self.loan_term = loan_term
        self.application_date = application_date
        self.interest_rate = interest_rate
        self.name = name
        self.personal_id = personal_id

    def serialize(self) -> dict:
        return {
            'loan_amount': self.loan_amount,
            'loan_term': self.loan_term,
            'application_date': self.application_date,
            'interest_rate': self.interest_rate,
            'name': self.name,
            'personal_id': self.personal_id
        }
