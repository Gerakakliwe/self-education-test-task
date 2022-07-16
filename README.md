# self-education-test-task
Test task for the third checkpoint.

# Dev setup
git clone git@github.com:Gerakakliwe/self-education-test-task.git
cd self-education-test-task
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install connexion[swagger-ui]
python server.py
# After those steps - check the http://127.0.0.1:5000

# Database
# If you want/have to create default database - run:
python build_database.py

# Tests
# Due to the structure of a program - You have to run tests using test classes like that:
python -m unittest test_employees.TestEmployeeRead
python -m unittest test_employees.TestEmployeeCreate
python -m unittest test_employees.TestEmployeeUpdate
python -m unittest test_employees.TestEmployeeDelete

