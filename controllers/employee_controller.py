# requires authentication
from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.employee import Employee, employees_schema, employee_schema


employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

# http://localhost:8080/employees - GET
@employees_bp.route('/')
def get_all_employees():
    stmt = db.select(Employee)
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
    
@employees_bp.route("/", methods=["POST"])
# @jwt_required()
def create_employee():
    body_data = employee_schema.load(request.get_json())
    # Create a new employee model instance
    employee = Employee(
        role = body_data.get('role'),
        hire_date = date.today(),
        years = body_data.get('years'),
        work_department = body_data.get('work_department'),
        education_level = body_data.get('educational_level'),
        salary = body_data.get('salary'),
        bonus = body_data.get('bonus'),
        commission = body_data.get('comission'),
        leave = body_data.get('leave'),
        leave_sick = body_data.get('leave_sick'),
        leave_parental = body_data.get('leave_parental'),
    )
    # Add that to the session and commit
    db.session.add(employee)
    db.session.commit()
    # return the newly created employee
    return employee_schema.dump(employee), 201

@employees_bp.route('/<int:employee_id>', methods=["DELETE"])
def delete_employee(employee_id):
    stmt = db.select(Employee).where(Employee.id == employee_id)
    employee = db.session.scalar(stmt)
    # if employee exists
    if employee:
        # delete the employee from the session and commit
        db.session.delete(employee)
        db.session.commit()
        # return msg
        return {'message': f"Employee '{employee.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Employee with id {employee_id} not found"}, 404
    

# http://localhost:8080/employees/5 - PUT, PATCH
@employees_bp.route('/<int:employee_id>', methods=["PUT", "PATCH"])
def update_employee(employee_id):
    # Get the data to be updated from the body of the request
    body_data = employee_schema.load(request.get_json(), partial=True)
    # Get the employee from the db whose fields need to be updated
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    # if employee exists
    if employee:
        # if str(employee.user_id) != get_jwt_identity(): # Integer Field Vs String Field
        #     return {"error": "Only the owner can edit the employee"}, 403
        # # update the fields

        employee.role = body_data.get('role') or employee.role
        employee.years = body_data.get('years') or employee.years
        employee.work_department = body_data.get('work_department') or employee.work_department
        employee.education_level = body_data.get('educational_level') or employee.education_level
        employee.salary = body_data.get('salary') or employee.salary
        employee.bonus = body_data.get('bonus') or employee.bonus
        employee.commission = body_data.get('comission') or employee.commission
        employee.leave = body_data.get('leave') or employee.leave
        employee.leave_sick = body_data.get('leave_sick') or employee.leave_sick
        employee.leave_parental = body_data.get('leave_parental') or employee.leave_parental

        # commit the changes
        db.session.commit()
        # return the updated employee back
         
        return employee_schema.dump(employee)

    # else
    else:
        # return error msg
        return {'error': f'Employee with id {employee_id} not found'}, 404