import os
from config import db
from models import Employee

# Data to initialize database with
EMPLOYEES = [
    {"fname": "Pavel", "lname": "Yemelianov", "position": "SD2", "computer_name": "p.yemelianov-desktop"},
    {"fname": "Andrey", "lname": "Samodin", "position": "QA", "computer_name": "a.samodin-desktop"},
    {"fname": "Oleg", "lname": "Fomenko", "position": "SD5", "computer_name": "o.fomenko-desktop"}
]


# Function that will create and fill database
def create_database():
    # Delete database file if it already exists
    if os.path.exists("employees.db"):
        os.remove("employees.db")

    # Create the database
    db.create_all()

    # Iterate over the EMPLOYEES structure and populate the database
    for employee in EMPLOYEES:
        e = Employee(lname=employee.get("lname"),
                     fname=employee.get("fname"),
                     position=employee.get("position"),
                     computer_name=employee.get("computer_name")
                     )
        db.session.add(e)

    db.session.commit()


# Create database when we run this script
create_database()
