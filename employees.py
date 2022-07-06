"""
This is the employees module that supports all the REST actions for the employees data
"""
from config import db
from flask import (
    make_response,
    abort
)
from models import (
    Employee,
    EmployeeSchema
)


def read_all():
    """
    This function responds to a request for /api/employees
    with the complete list of employees

    :return:    json string of list of people
    """
    # Create the list of people from our data
    employees = Employee.query.order_by(Employee.lname).all()

    # Serialize the data for the response
    employees_schema = EmployeeSchema(many=True)
    data = employees_schema.dump(employees)
    return data