from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.workorder_comment import Workorder_Comment, workorder_comments_schema, workorder_comment_schema


workorder_comments_bp = Blueprint('workorder_comments', __name__, url_prefix='/workorder_comments')

# http://localhost:8080/workorder_comments - GET
@workorder_comments_bp.route('/')
def get_all_workorder_comments():
    stmt = db.select(Workorder_Comment).order_by(Workorder_Comment.date_created.desc())
    workorder_comments = db.session.scalars(stmt)
    return workorder_comments_schema.dump(workorder_comments)

# http://localhost:8080/workorder_comments/*id - GET
@workorder_comments_bp.route('/<int:workorder_comment_id>')
def get_one_card(workorder_comment_id): # card_id = *id
    stmt = db.select(Workorder_Comment).filter_by(id=workorder_comment_id) # select * from workorder_comments where id=*id
    workorder_comment = db.session.scalar(stmt)
    if workorder_comment:
        return workorder_comment_schema.dump(workorder_comment)
    else:
        return {"error": f"Card with id {workorder_comment_id} not found"}, 404
    
@workorder_comments_bp.route("/", methods=["POST"])
# @jwt_required()
def create_workorder_comment():
    body_data = workorder_comment_schema.load(request.get_json())
    # Create a new workorder_comment model instance
    workorder_comment = Workorder_Comment(
        workorder_id = body_data.get('workorder_id'),
        employee_id = body_data.get('employee_id'),
        title = body_data.get('title'),
        message = body_data.get('message'),
        date_created = date.today(),
        date_modified = body_data.get('date_modified')
    )
    # Add that to the session and commit
    db.session.add(workorder_comment)
    db.session.commit()
    # return the newly created workorder_comment
    return workorder_comment_schema.dump(workorder_comment), 201

@workorder_comments_bp.route('/<int:workorder_comment_id>', methods=["DELETE"])
def delete_workorder_comment(workorder_comment_id):
    stmt = db.select(Workorder_Comment).where(Workorder_Comment.id == workorder_comment_id)
    workorder_comment = db.session.scalar(stmt)
    # if workorder_comment exists
    if workorder_comment:
        # delete the workorder_comment from the session and commit
        db.session.delete(workorder_comment)
        db.session.commit()
        # return msg
        return {'message': f"Workorder_Comment '{workorder_comment.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Workorder_Comment with id {workorder_comment_id} not found"}, 404
    

# http://localhost:8080/workorder_comments/5 - PUT, PATCH
@workorder_comments_bp.route('/<int:workorder_comment_id>', methods=["PUT", "PATCH"])
def update_workorder_comment(workorder_comment_id):
    # Get the data to be updated from the body of the request
    body_data = workorder_comment_schema.load(request.get_json(), partial=True)
    # Get the workorder_comment from the db whose fields need to be updated
    stmt = db.select(Workorder_Comment).filter_by(id=workorder_comment_id)
    workorder_comment = db.session.scalar(stmt)
    # if workorder_comment exists
    if workorder_comment:
        # if str(workorder_comment.user_id) != get_jwt_identity(): # Integer Field Vs String Field
        #     return {"error": "Only the owner can edit the workorder_comment"}, 403
        # # update the fields
        workorder_comment.workorder_id = body_data.get('workorder_id') or workorder_comment.workorder_id
        workorder_comment.employee_id = body_data.get('employee_id') or workorder_comment.employee_id
        workorder_comment.title = body_data.get('title') or workorder_comment.title
        workorder_comment.message = body_data.get('message') or workorder_comment.message
        workorder_comment.date_modified = body_data.get('date_modified') or workorder_comment.date_modified

        # commit the changes
        db.session.commit()
        # return the updated workorder_comment back
         
        return workorder_comment_schema.dump(workorder_comment)

    # else
    else:
        # return error msg
        return {'error': f'Workorder_Comment with id {workorder_comment_id} not found'}, 404