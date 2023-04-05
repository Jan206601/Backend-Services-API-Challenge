import os
import sqlite3
from typing import List

from loan_application import LoanApplication

SQLITE_DB_PATH = 'loans.db'


class DAO:
    def __init__(self):
        new_db_file = not os.path.isfile(SQLITE_DB_PATH)

        db_connection = self.__get_connection()
        db_cursor = db_connection.cursor()

        # If creating a new database, define the schema
        if new_db_file:
            # Create loans table
            db_cursor.execute('''CREATE TABLE loans
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          loan_amount REAL,
                          loan_term INTEGER,
                          application_date TEXT,
                          interest_rate REAL,
                          name TEXT,
                          personal_id TEXT)''')
            # Create blacklist table
            db_cursor.execute('''CREATE TABLE blacklist
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          personal_id TEXT,
                          UNIQUE (personal_id))''')
            db_connection.commit()

    @staticmethod
    def __get_connection():
        db_connection = sqlite3.connect(SQLITE_DB_PATH)
        return db_connection

    def add_loan_application(self, loan_application: LoanApplication):
        db_connection = self.__get_connection()
        db_connection.cursor().execute(
            "INSERT INTO loans (loan_amount, loan_term, application_date, interest_rate, name, personal_id)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (loan_application.loan_amount, loan_application.loan_term, loan_application.application_date,
             loan_application.interest_rate, loan_application.name, loan_application.personal_id))
        db_connection.commit()

    def get_loan_applications(self, personal_id) -> List[LoanApplication]:
        db_connection = self.__get_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM loans WHERE personal_id=?", (personal_id,))
        fetch_result = db_cursor.fetchall()
        loans = []
        for loan in fetch_result:
            loans.append(LoanApplication(loan[1], loan[2], loan[3], loan[4], loan[5], loan[6]))
        return loans

    def person_in_blacklist(self, personal_id) -> bool:
        db_connection = self.__get_connection()
        query = db_connection.cursor().execute("SELECT * FROM blacklist WHERE personal_id=?", (personal_id,))
        return query.fetchone() is not None
