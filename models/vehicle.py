from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp
from marshmallow.exceptions import ValidationError

from init import db, ma

#VALID_GEARBOXES = ('To Do', 'Ongoing', 'Done', 'Testing', 'Deployed')
#VALID_TRANSMISSIONS = ('Low', 'Medium', 'High', 'Urgent')

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id  = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    licence_num = db.Column(db.String)
    registered = db.Column(db.Boolean, default=False)
    status = db.Column(db.String) # STORE IN WORKORDERS???

    owner_Prev = db.Column(db.String)
    second_hand = db.Column(db.Boolean, default=False)
    
    num_kilometer = db.Column(db.Integer)
    num_key = db.Column(db.Integer)

    model_price = db.Column(db.Numeric)
    model_manufacturer = db.Column(db.String)
    model_name = db.Column(db.String)
    model_year = db.Column(db.Integer)
    model_type = db.Column(db.String)
    model_fuel_type = db.Column(db.String)
    model_fuel_capacity = db.Column(db.Integer)
    model_fuel_consumption = db.Column(db.Integer)
    model_powerplant = db.Column(db.String)
    model_transmission = db.Column(db.String)
    model_gearbox = db.Column(db.String)
    model_weight = db.Column(db.Integer)
    model_color = db.Column(db.String)

    visible = db.Column(db.Boolean, default=True) # set to false when in customer_order???

    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)

    #vehicle_workorders = db.relationship('Vehicle_Workorder', back_populates='vehicle', cascade='all, delete')
    location = db.relationship('Location', back_populates='vehicles')
    customer_order = db.relationship('Customer_Order', back_populates='vehicle', cascade='all, delete') #Only 1 vehicle per order + delete orders if vehicle is removed
    workorders = db.relationship('Workorder', back_populates='vehicle', cascade='all, delete')
    #workorder_comments = db.relationship('Workorder', back_populates='vehicle' cascade='all, delete')
    

class VehicleSchema(ma.Schema):    
    vin = fields.String(required=True, validate=And(
        Length(min=17, error="VIN requires 17 alphanumeric characters excluding: I, O, and Q"),
        Regexp('^[A-HJ-NPR-Z0-9]{17}$', error="VIN can only have alphanumeric characters excluding: I, O, and Q")
    ))

    #vehicle_workorders
    location = fields.Nested('LocationSchema', only = ['id', 'address1']) #can only have 1 location
    customer_order = fields.Nested('Customer_OrderSchema', exclude=['vehicle']) #can only have 1 customer_order
    workorders = fields.List(fields.Nested('WorkorderSchema', exclude=['vehicle']))#multi workorders
    #workorder_comments = fields.List(fields.Nested('WorkorderSchema', exclude=['vehicle']))#multi comments



    class Meta:
        fields = ('id', 'vin', 'model_price', 'model_manufacturer', 'model_name', 'model_year', 'model_type', 'model_fuel_type', 'model_fuel_capacity', 'model_fuel_consumption', 'model_powerplant', 'model_transmission', 'model_gearbox', 'model_weight', 'model_color')
        ordered = True

vehicle_schema = VehicleSchema() # {}
vehicles_schema = VehicleSchema(many=True) # [{}, {}, {}]