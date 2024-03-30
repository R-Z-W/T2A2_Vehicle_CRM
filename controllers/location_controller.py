from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.location import Location, locations_schema, location_schema


locations_bp = Blueprint('locations', __name__, url_prefix='/locations')

# http://localhost:8080/locations - GET
@locations_bp.route('/')
def get_all_locations():
    stmt = db.select(Location)
    locations = db.session.scalars(stmt)
    return locations_schema.dump(locations)

# http://localhost:8080/locations/*id - GET
@locations_bp.route('/<int:location_id>')
def get_one_card(location_id): # card_id = *id
    stmt = db.select(Location).filter_by(id=location_id) # select * from locations where id=*id
    location = db.session.scalar(stmt)
    if location:
        return location_schema.dump(location)
    else:
        return {"error": f"Card with id {location_id} not found"}, 404
    
@locations_bp.route("/", methods=["POST"])
# @jwt_required()
def create_location():
    body_data = location_schema.load(request.get_json())
    # Create a new location model instance
    location = Location(
        address1 = body_data.get('address1'),
        address2 = body_data.get('address2'),
        city = body_data.get('city'),
        postal_code = body_data.get('postal_code'),
        state = body_data.get('state'),
        country = body_data.get('country')
    )
    # Add that to the session and commit
    db.session.add(location)
    db.session.commit()
    # return the newly created location
    return location_schema.dump(location), 201

@locations_bp.route('/<int:location_id>', methods=["DELETE"])
def delete_location(location_id):
    stmt = db.select(Location).where(Location.id == location_id)
    location = db.session.scalar(stmt)
    # if location exists
    if location:
        # delete the location from the session and commit
        db.session.delete(location)
        db.session.commit()
        # return msg
        return {'message': f"Location '{location.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Location with id {location_id} not found"}, 404
    

# http://localhost:8080/locations/5 - PUT, PATCH
@locations_bp.route('/<int:location_id>', methods=["PUT", "PATCH"])
def update_location(location_id):
    # Get the data to be updated from the body of the request
    body_data = location_schema.load(request.get_json(), partial=True)
    # Get the location from the db whose fields need to be updated
    stmt = db.select(Location).filter_by(id=location_id)
    location = db.session.scalar(stmt)
    # if location exists
    if location:
        # if str(location.user_id) != get_jwt_identity(): # Integer Field Vs String Field
        #     return {"error": "Only the owner can edit the location"}, 403
        # # update the fields
        location.address1 = body_data.get('address1') or location.address1
        location.address2 = body_data.get('address2') or location.address2
        location.city = body_data.get('city') or location.city
        location.postal_code = body_data.get('postal_code') or location.postal_code
        location.state = body_data.get('state') or location.state
        location.country = body_data.get('country') or location.country

        # commit the changes
        db.session.commit()
        # return the updated location back
         
        return location_schema.dump(location)

    # else
    else:
        # return error msg
        return {'error': f'Location with id {location_id} not found'}, 404