from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.workorder import Workorder, workorders_schema, workorder_schema


workorders_bp = Blueprint('workorders', __name__, url_prefix='/workorders')

# http://localhost:8080/workorders - GET
@workorders_bp.route('/')
def get_all_workorders():
    stmt = db.select(Workorder).order_by(Workorder.date_created.desc())
    workorders = db.session.scalars(stmt)
    return workorders_schema.dump(workorders)

# http://localhost:8080/workorders/*id - GET
@workorders_bp.route('/<int:workorder_id>')
def get_one_card(workorder_id): # card_id = *id
    stmt = db.select(Workorder).filter_by(id=workorder_id) # select * from workorders where id=*id
    workorder = db.session.scalar(stmt)
    if workorder:
        return workorder_schema.dump(workorder)
    else:
        return {"error": f"Card with id {workorder_id} not found"}, 404
    

@workorders_bp.route("/", methods=["POST"])
# @jwt_required()
def create_workorder():
    body_data = workorder_schema.load(request.get_json())
    # Create a new workorder model instance
    workorder = Workorder(
        vehicle_id = body_data.get('vehicle_id'),
        employee_id = body_data.get('employee_id'),
        status = body_data.get('status'),
        title = body_data.get('title'),
        description = body_data.get('description'),
        date_created = date.today(),
        date_completed = body_data.get('date_completed')
    )

    # Add that to the session and commit
    db.session.add(workorder)
    db.session.commit()
    # return the newly created workorder
    return workorder_schema.dump(workorder), 201

@workorders_bp.route('/<int:workorder_id>', methods=["DELETE"])
def delete_workorder(workorder_id):
    stmt = db.select(Workorder).where(Workorder.id == workorder_id)
    workorder = db.session.scalar(stmt)
    # if workorder exists
    if workorder:
        # delete the workorder from the session and commit
        db.session.delete(workorder)
        db.session.commit()
        # return msg
        return {'message': f"Workorder '{workorder.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Workorder with id {workorder_id} not found"}, 404
    

# http://localhost:8080/workorders/5 - PUT, PATCH
@workorders_bp.route('/<int:workorder_id>', methods=["PUT", "PATCH"])
def update_workorder(workorder_id):
    # Get the data to be updated from the body of the request
    body_data = workorder_schema.load(request.get_json(), partial=True)
    # Get the workorder from the db whose fields need to be updated
    stmt = db.select(Workorder).filter_by(id=workorder_id)
    workorder = db.session.scalar(stmt)
    # if workorder exists
    if workorder:

        workorder.vehicle_id = body_data.get('vehicle_id') or workorder.vehicle_id
        workorder.employee_id = body_data.get('employee_id') or workorder.employee_id
        workorder.status = body_data.get('status') or workorder.status
        workorder.title = body_data.get('title') or workorder.title
        workorder.description = body_data.get('description') or workorder.description
        workorder.date_completed = body_data.get('date_completed') or workorder.date_completed

        # commit the changes
        db.session.commit()
        # return the updated workorder back
         
        return workorder_schema.dump(workorder)

    # else
    else:
        # return error msg
        return {'error': f'Workorder with id {workorder_id} not found'}, 404