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