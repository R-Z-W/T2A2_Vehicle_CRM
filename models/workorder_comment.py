from init import db, ma
from marshmallow import fields

class Workorder_Comment(db.Model):
    __tablename__ = "workorder_comments"

    id = db.Column(db.Integer, primary_key=True)
    workorder_id = db.Column(db.Integer, db.ForeignKey("workorders.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    title = db.Column(db.String)
    message = db.Column(db.Text)

    date_created = db.Column(db.Date, nullable=False)
    date_modified = db.Column(db.Date)

    workorder = db.relationship('Workorder', back_populates='workorder_comments')
    employee = db.relationship('Employee', back_populates='workorder_comments')

class Workorder_CommentSchema(ma.Schema):
    
    workorder = fields.Nested('WorkorderSchema', only=['id'])
    employee = fields.Nested('EmployeeSchema', only=['id'])

    class Meta:
        fields = ('id', 'workorder', 'employee', 'title', 'message', 'date_created', 'date_modified')

workorder_comment_schema = Workorder_CommentSchema()
workorder_comments_schema = Workorder_CommentSchema(many=True)