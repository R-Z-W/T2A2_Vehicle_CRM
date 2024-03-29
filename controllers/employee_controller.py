# requires authentication

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.employee import Employee, employees_schema, employee_schema


employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

# http://localhost:8080/employees - GET
@employees_bp.route('/')
def get_all_employees():
    stmt = db.select(Employee).order_by(Employee.role.desc())
    employees = db.session.scalars(stmt)
    return employees_schema.dump(employees)

# http://localhost:8080/employees/*id - GET
@employees_bp.route('/<int:employee_id>')
def get_one_card(employee_id): # card_id = *id
    stmt = db.select(Employee).filter_by(id=employee_id) # select * from employees where id=*id
    employee = db.session.scalar(stmt)
    if employee:
        return employee_schema.dump(employee)
    else:
        return {"error": f"Card with id {employee_id} not found"}, 404