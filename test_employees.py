import unittest
from unittest.mock import patch
from employees import (
    read_all,
    read_one,
    update,
    delete,
    create
)

# Data to compare with read one from database
EMPLOYEES = [
    {"employee_id": 1, "fname": "Pavel", "lname": "Yemelianov", "position": "SD2", "computer_name": "p.yemelianov-desktop"},
    {"employee_id": 2, "fname": "Andrey", "lname": "Samodin", "position": "QA", "computer_name": "a.samodin-desktop"},
    {"employee_id": 3, "fname": "Oleg", "lname": "Fomenko", "position": "SD5", "computer_name": "o.fomenko-desktop"}
]

# Data to use in test create function
EMPLOYEE_TO_CREATE = {
    "employee_id": 4,
    "fname": "test_fname",
    "lname": "test_lname",
    "position": "test_position",
    "computer_name": "test_computer_name"
}

# Data to use in test update` function
EMPLOYEE_TO_UPDATE = {
    "employee_id": 1,
    "fname": "update_fname",
    "lname": "update_lname",
    "position": "update_position",
    "computer_name": "update_computer_name"
}


# Tests for read functions
class TestEmployeeRead(unittest.TestCase):
    def test_read_all(self):
        result = read_all()
        self.assertEqual(result, EMPLOYEES)

    def test_read_one_should_succeed(self):
        result = read_one(1)
        self.assertEqual(result, EMPLOYEES[0])

    @patch('employees.abort')
    def test_read_nonexistent_one_should_fail(self, abort_mock):
        id_to_read = 999
        read_one(id_to_read)
        abort_mock.assert_called_once_with(404, f'Employee with ID {id_to_read} was not found')


# Tests for create functions
class TestEmployeeCreate(unittest.TestCase):
    def test_create_nonexistent_should_succeed(self):
        result = create(EMPLOYEE_TO_CREATE)
        self.assertEqual(result, (EMPLOYEE_TO_CREATE, 201))

    @patch('employees.abort')
    def test_create_that_exist_should_fail(self, abort_mock):
        create(EMPLOYEE_TO_CREATE)
        abort_mock.assert_called_once_with(406,
                                           f"Employee {EMPLOYEE_TO_CREATE.get('fname')}, "
                                           f"{EMPLOYEE_TO_CREATE.get('lname')} already exists")


# Tests for update functions
class TestEmployeeUpdate(unittest.TestCase):
    def test_update_employee_found_should_succeed(self):
        id_to_update = 1
        result = update(id_to_update, EMPLOYEE_TO_UPDATE)
        self.assertEqual(result, (EMPLOYEE_TO_UPDATE, 200))

    @patch('employees.abort')
    def test_update_employee_not_found_should_fail(self, abort_mock):
        id_to_update = 999
        update(id_to_update, EMPLOYEE_TO_UPDATE)
        abort_mock.assert_called_once_with(404, f"Employee with ID {id_to_update} was not found")

    @patch('employees.abort')
    def test_update_employee_whose_name_exists_should_fail(self, abort_mock):
        id_to_update = 3
        update(id_to_update, EMPLOYEE_TO_UPDATE)
        abort_mock.assert_called_once_with(409,
                                           f"Employee {EMPLOYEE_TO_UPDATE.get('fname')}, "
                                           f"{EMPLOYEE_TO_UPDATE.get('lname')} already exists")


# Tests for delete functions
class TestEmployeeDelete(unittest.TestCase):
    @patch('employees.make_response')
    def test_delete_one_should_succeed(self, make_response_mock):
        id_to_delete = 1
        delete(id_to_delete)
        make_response_mock.assert_called_once_with(f"Employee {id_to_delete} successfully deleted", 200)

    @patch('employees.abort')
    def test_delete_nonexistent_one_should_fail(self, abort_mock):
        id_to_delete = 999
        delete(id_to_delete)
        abort_mock.assert_called_once_with(404, f"Employee with ID {id_to_delete} was not found")
