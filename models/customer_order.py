from init import db, ma
from marshmallow import fields

class Customer_Order(db.Model):
    __tablename__ = "customer_orders"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    #location_billing_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    #sales_employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    date_created = db.Column(db.Date)
    date_delivered = db.Column(db.Date)
    status = db.Column(db.String)
    
    location = db.relationship('Location', back_populates='customer_orders')
    customer = db.relationship('Customer', back_populates='customer_orders') #Customer can have multiple orders
    vehicle = db.relationship('Vehicle', back_populates='customer_order') #Only 1 order per vehicle
    #employee = db.relationship('Employee', back_populates='customer_order', uselist=False)
    

class Customer_OrderSchema(ma.Schema):
    location = fields.Nested('LocationSchema', only=['id', 'address1', 'postal_code']) #can only have 1 location
    customer = fields.Nested('CustomerSchema', only=['id','fname', 'lname', 'phone_num']) #can only have 1 customer
    vehicle = fields.Nested('VehicleSchema', only=['id', 'model_name', 'model_price']) #can only have 1 vehicle 
    #employee = fields.Nested('EmployeeSchema', only=['fname', 'lname'])
    

    # Relevant Data To Be Sent
    class Meta:
        fields = ('id', 'location', 'customer', 'vehicle', 'date_created', 'date_delivered')


customer_order_schema = Customer_OrderSchema()
customer_orders_schema =  Customer_OrderSchema(many=True)