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