from config import (
    db,
    ma
)


class Employee(db.Model):
    __tablename__ = "employee"
    employee_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    position = db.Column(db.String(32))
    computer_name = db.Column(db.String(32))


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        sqla_session = db.session
        load_instance = True
