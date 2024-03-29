from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.vehicle import Vehicle, vehicles_schema, vehicle_schema


vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/vehicles')

# http://localhost:8080/vehicles - GET
@vehicles_bp.route('/')
def get_all_vehicles():
    stmt = db.select(Vehicle)
    vehicles = db.session.scalars(stmt)
    return vehicles_schema.dump(vehicles)

# http://localhost:8080/vehicles/*id - GET
@vehicles_bp.route('/<int:vehicle_id>')
def get_one_card(vehicle_id): # card_id = *id
    stmt = db.select(Vehicle).filter_by(id=vehicle_id) # select * from vehicles where id=*id
    vehicle = db.session.scalar(stmt)
    if vehicle:
        return vehicle_schema.dump(vehicle)
    else:
        return {"error": f"Card with id {vehicle_id} not found"}, 404