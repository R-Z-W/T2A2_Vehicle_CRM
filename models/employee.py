from marshmallow import fields
from init import db, ma

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    #is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String)
    hire_date = db.Column(db.Date)
    years = db.Column(db.Integer)
    work_department = db.Column(db.String)
    education_level = db.Column(db.String)
    salary = db.Column(db.Numeric)
    bonus = db.Column(db.Numeric)
    commission = db.Column(db.Numeric)
    leave = db.Column(db.Numeric)
    leave_sick = db.Column(db.Numeric)
    leave_parental = db.Column(db.Numeric)

    #department_id = db.Column(db.Integerdb.Integer, db.ForeignKey('department.id'), nullable=False)
    
    #Cannot Get self referencing Foreign Key to work in Controller (Need To Store Employees First Then Create Relationship)
    #supervisor_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    #supervisor = db.relationship('Employee', remote_side=id, backref='employees')

    customer = db.relationship('Customer', back_populates='employee')
    #customer_orders = db.relationship('Customer_Order', back_populates='employee', cascade='all, delete')
    workorders = db.relationship('Workorder', back_populates='employee', cascade='all, delete')
    workorder_comments = db.relationship('Workorder_Comment', back_populates='employee', cascade='all, delete')
   


class EmployeeSchema(ma.Schema):    
   
    # employee = fields.Nested('EmployeeSchema', only=['id', 'fname', 'lname', 'phone_num'])
    # customer_orders = fields.List(fields.Nested('Customer_OrderSchema', exclude=['employee']))

    customer = fields.List(fields.Nested('CustomerSchema', exclude=['employee']))
    workorders = fields.List(fields.Nested('WorkorderSchema', exclude=['employee']))#multi workorders
    workorder_comments = fields.List(fields.Nested('Workorder_CommentSchema', exclude=['employee']))#multi comments

    class Meta:
        fields = ('id', 'role', 'work_department')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema() 