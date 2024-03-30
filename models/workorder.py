from marshmallow import fields
from marshmallow.validate import OneOf

from init import db, ma

VALID_STATUSES = ('Available', 'UnAvailable', 'InProgress', 'Complete')

class Workorder(db.Model):
    __tablename__ = "workorders"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    status = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date, nullable=False)
    date_completed = db.Column(db.Date)
    
    vehicle = db.relationship('Vehicle', back_populates='workorders')
    employee = db.relationship('Employee', back_populates='workorders')
    
    workorder_comments = db.relationship('Workorder_Comment', back_populates='workorder', cascade='all, delete')

class WorkorderSchema(ma.Schema):
    
    status = fields.String(validate=OneOf(VALID_STATUSES))
    
    vehicle = fields.Nested('VehicleSchema', only=['id'])
    employee = fields.Nested('EmployeeSchema', only=['id'])
    workorder_comments = fields.List(fields.Nested('Workorder_CommentSchema', exclude=['workorder']))


    class Meta:
        fields = ('id', 'employee_id', 'vehicle_id', 'status', 'title', 'description', 'date_created', 'date_completed')
        ordered = True

workorder_schema = WorkorderSchema()
workorders_schema =  WorkorderSchema(many=True)