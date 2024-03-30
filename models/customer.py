from init import db, ma
from marshmallow import fields

class Customer(db.Model):
    __tablename__ = "customers"

    id  = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    gender = db.Column(db.String)
    birth_date = db.Column(db.Date)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_num = db.Column(db.Integer)
    licence_num = db.Column(db.Integer, nullable=False, unique=True)
    #last_viewed_vehicles = db.Column(db.String) # String of IDs seperated by commas, max 6 last viewed vehicles
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False) #not good idea as customer may accidentaly be given admin rights (consider putting in employee model)
    
    bank_id = db.Column(db.Integer, db.ForeignKey("banks.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    
    
    bank = db.relationship('Bank', back_populates='customers', cascade='all, delete')
    location = db.relationship('Location', back_populates='customers')
    employee = db.relationship('Employee', back_populates='customer', cascade='all, delete')    
    customer_orders = db.relationship('Customer_Order', back_populates='customer', cascade='all, delete')

class CustomerSchema(ma.Schema):    
    #workorders = fields.List(fields.Nested('CardSchema', exclude=['user']))
    #workorder_comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))
    bank = fields.Nested('BankSchema', only = ['id']) # can only have 1 bank (for now)
    location = fields.Nested('LocationSchema', only=['id', 'city']) #can only have 1 location
    employee = fields.Nested('EmployeeSchema', only=['id']) #can only have 1 employee (for now)
    customer_orders = fields.List(fields.Nested('Customer_OrderSchema', exclude=['customer'])) # multi orders at 1 customer

    class Meta:
        fields = ('id', 'fname', 'lname', 'gender', 'birth_date', 'email', 'phone_num', 'licence_num', 'password', 'is_admin', 'bank_id', 'location_id', 'employee_id')
customer_schema = CustomerSchema(exclude=['password']) # {}
customers_schema = CustomerSchema(many=True, exclude=['password']) # [{}, {}, {}]