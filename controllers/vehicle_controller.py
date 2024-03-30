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
    

@vehicles_bp.route("/", methods=["POST"])
# @jwt_required()
def create_vehicle():
    body_data = vehicle_schema.load(request.get_json())
    # Create a new vehicle model instance
    vehicle = Vehicle(
        vin = body_data.get('vin'),
        licence_num = body_data.get('licence_num'),
        registered = body_data.get('registered'),
        status = body_data.get('status'),
        owner_Prev = body_data.get('owner_Prev'),
        second_hand = body_data.get('second_hand'),
        num_kilometer = body_data.get('num_kilometer'),
        num_key = body_data.get('num_key'),
        model_price = body_data.get('model_price'),
        model_manufacturer = body_data.get('model_manufacturer'),
        model_name = body_data.get('model_name'),
        model_year = body_data.get('model_year'),
        model_type = body_data.get('model_type'),
        model_fuel_type = body_data.get('model_fuel_type'),
        model_fuel_capacity = body_data.get('model_fuel_capacity'),
        model_fuel_consumption = body_data.get('model_fuel_consumption'),
        model_powerplant = body_data.get('model_powerplant'),
        model_transmission = body_data.get('model_transmission'),
        model_gearbox = body_data.get('model_gearbox'),
        model_weight = body_data.get('model_weight'),
        model_color = body_data.get('model_color'),
        visible = body_data.get('visible'),
        location_id = body_data.get('location_id')
    )
    # Add that to the session and commit
    db.session.add(vehicle)
    db.session.commit()
    # return the newly created vehicle
    return vehicle_schema.dump(vehicle), 201

@vehicles_bp.route('/<int:vehicle_id>', methods=["DELETE"])
def delete_vehicle(vehicle_id):
    stmt = db.select(Vehicle).where(Vehicle.id == vehicle_id)
    vehicle = db.session.scalar(stmt)
    # if vehicle exists
    if vehicle:
        # delete the vehicle from the session and commit
        db.session.delete(vehicle)
        db.session.commit()
        # return msg
        return {'message': f"Vehicle '{vehicle.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Vehicle with id {vehicle_id} not found"}, 404
    

# http://localhost:8080/vehicles/5 - PUT, PATCH
@vehicles_bp.route('/<int:vehicle_id>', methods=["PUT", "PATCH"])
def update_vehicle(vehicle_id):
    # Get the data to be updated from the body of the request
    body_data = vehicle_schema.load(request.get_json(), partial=True)
    # Get the vehicle from the db whose fields need to be updated
    stmt = db.select(Vehicle).filter_by(id=vehicle_id)
    vehicle = db.session.scalar(stmt)
    # if vehicle exists
    if vehicle:
        vehicle.vin = body_data.get('vin') or vehicle.vin
        vehicle.licence_num = body_data.get('licence_num') or vehicle.licence_num
        vehicle.registered = body_data.get('registered') or vehicle.registered
        vehicle.status = body_data.get('status') or vehicle.status
        vehicle.owner_Prev = body_data.get('owner_Prev') or vehicle.owner_Prev
        vehicle.second_hand = body_data.get('second_hand') or vehicle.second_hand
        vehicle.num_kilometer = body_data.get('num_kilometer') or vehicle.num_kilometer
        vehicle.num_key = body_data.get('num_key') or vehicle.num_key
        vehicle.model_price = body_data.get('model_price') or vehicle.model_price
        vehicle.model_manufacturer = body_data.get('model_manufacturer') or vehicle.model_manufacturer
        vehicle.model_name = body_data.get('model_name') or vehicle.model_name
        vehicle.model_year = body_data.get('model_year') or vehicle.model_year
        vehicle.model_type = body_data.get('model_type') or vehicle.model_type
        vehicle.model_fuel_type = body_data.get('model_fuel_type') or vehicle.model_fuel_type
        vehicle.model_fuel_capacity = body_data.get('model_fuel_capacity') or vehicle.model_fuel_capacity
        vehicle.model_fuel_consumption = body_data.get('model_fuel_consumption') or vehicle.model_fuel_consumption
        vehicle.model_powerplant = body_data.get('model_powerplant') or vehicle.model_powerplant
        vehicle.model_transmission = body_data.get('model_transmission') or vehicle.model_transmission
        vehicle.model_gearbox = body_data.get('model_gearbox') or vehicle.model_gearbox
        vehicle.model_weight = body_data.get('model_weight') or vehicle.model_weight
        vehicle.model_color = body_data.get('model_color') or vehicle.model_color
        vehicle.visible = body_data.get('visible') or vehicle.visible
        vehicle.location_id = body_data.get('location_id') or vehicle.location_id
        # commit the changes
        db.session.commit()
        # return the updated vehicle back
         
        return vehicle_schema.dump(vehicle)

    # else
    else:
        # return error msg
        return {'error': f'Vehicle with id {vehicle_id} not found'}, 404