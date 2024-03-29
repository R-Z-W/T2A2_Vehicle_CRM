from init import db, ma
from marshmallow import fields


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    state = db.Column(db.String)
    country = db.Column(db.String)

    vehicles = db.relationship('Vehicle', back_populates='location')
    customers = db.relationship('Customer', back_populates='location') # multi customers at 1 location
    customer_orders = db.relationship('Customer_Order', back_populates='location') # multi customers at 1 location
    #employee = db.relationship('Employee', back_populates='location')
    #vehicle = db.relationship('Vehicle', back_populates='location')

class LocationSchema(ma.Schema):
    vehicles = fields.List(fields.Nested('VehicleSchema', exclude=['location'])) # multi vehicles at 1 location
    customers = fields.List(fields.Nested('CustomerSchema', exclude=['location'])) # multi customers at 1 location
    customer_orders = fields.List(fields.Nested('Customer_OrderSchema', exclude=['location'])) # multi orders at 1 location

    class Meta:
        fields = ('id', 'address1', 'address2', 'city', 'postal_code', 'state', 'country')

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)