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

    :return:    json string of list of employees
    """
    # Create the list of employees from our database
    employees = Employee.query.order_by(Employee.lname).all()

    # Serialize the data for the response
    employees_schema = EmployeeSchema(many=True)
    data = employees_schema.dump(employees)
    return data


def read_one(employee_id):
    """
    This function responds to a request for /api/employees/{employee_id}
    with one matching employee from employees
    :param employee_id:     Id of employee to find
    :return:                employee matching id
    """
    # Get the employee requested
    employee = Employee.query.filter(Employee.employee_id == employee_id).one_or_none()

    # Check if there is an employee with requested ID
    if employee is not None:

        # Serialize the data for the response
        employee_schema = EmployeeSchema()
        data = employee_schema.dump(employee)
        return data

    # Otherwise - we didn't find employee, throw an abort
    else:
        abort(
            404,
            f"Employee with id {employee_id} was not found"
        )


def create(employee):
    """
    This function creates a new employee in the database
    based on the passed employee data
    :param employee:    employee to create in database
    :return:            201 on success, 406 on employee exists
    """
    fname = employee.get("fname")
    lname = employee.get("lname")
    position = employee.get("position")
    computer_name = employee.get("computer_name")

    existing_employee = (
        Employee.query.filter(Employee.fname == fname)
        .filter(Employee.lname == lname)
        .filter(Employee.position == position)
        .filter(Employee.computer_name == computer_name)
        .one_or_none()
    )

    # Check if we can insert employee in database
    if existing_employee is None:

        # Create an employee instance using the schema and the passed in info
        schema = EmployeeSchema()
        new_employee = schema.load(employee, session=db.session)

        # Add the employee to the database
        db.session.add(new_employee)
        db.session.commit()

        # Serialize and return the newly created employee in response
        data = schema.dump(new_employee)

        return data, 201

    # Otherwise - no, employee already exists
    else:
        abort(
            406,
            f"Employee {fname}, {lname} already exists"
        )


def update(employee_id, employee):
    """
    This function updates an existing employee in the database
    Throws an error if an employee with the given name already
    exists in the database
    :param employee_id:   ID of the employee to update in the employees database
    :param employee:      employee to update
    :return:              updated employee
    """
    update_employee = Employee.query.filter(
        Employee.employee_id == employee_id
    ).one_or_none()

    # Try to find an existing employee with the same name as the update
    fname = employee.get("fname")
    lname = employee.get("lname")

    existing_employee = (
        Employee.query.filter(Employee.fname == fname)
        .filter(Employee.lname == lname)
        .one_or_none()
    )

    if update_employee is None:
        abort(
            404,
            f"Employee with ID {employee_id} was not found"
        )

    # Would our update create a duplicate of another employee
    elif (
            existing_employee is not None and existing_employee.employee_id != employee_id
    ):
        abort(
            409,
            f"Employee {fname}, {lname} already exists"
        )

    # Otherwise - ok, we can update
    else:

        # convert passed value into a db object
        schema = EmployeeSchema()
        update = schema.load(employee, session=db.session)

        # Set the ID to the employee we want to update
        update.employee_id = update_employee.employee_id

        # Merge the mew object into the old and commit it to the database
        db.session.merge(update)
        db.session.commit()

        # Return updated employee in the response
        data = schema.dump(update_employee)

        return data, 200


def delete(employee_id):
    """
    This function deletes an employee from the database
    :param employee_id:     ID of the employee to delete
    :return:                200 on successful delete, 404 if not found
    """
    # Get the employee requested
    employee = Employee.query.filter(Employee.employee_id == employee_id).one_or_none()

    # Did we find an employee
    if employee is not None:
        db.session.delete(employee)
        db.session.commit()
        return make_response(
            f"Employee {employee_id} successfully deleted", 200
        )

    # Otherwise - no employee, no one to delete
    else:
        abort(
            404,
            f"Employee with ID {employee_id} was not found"
        )
