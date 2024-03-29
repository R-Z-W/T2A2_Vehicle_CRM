#requires authentication


from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.customer_order import Customer_Order, customer_orders_schema, customer_order_schema


customer_orders_bp = Blueprint('customer_orders', __name__, url_prefix='/customer_orders')

# http://localhost:8080/customer_orders - GET
@customer_orders_bp.route('/')
def get_all_customer_orders():
    stmt = db.select(Customer_Order)
    customer_orders = db.session.scalars(stmt)
    return customer_orders_schema.dump(customer_orders)

# http://localhost:8080/customer_orders/*id - GET
@customer_orders_bp.route('/<int:customer_order_id>')
def get_one_card(customer_order_id): # card_id = *id
    stmt = db.select(Customer_Order).filter_by(id=customer_order_id) # select * from customer_orders where id=*id
    customer_order = db.session.scalar(stmt)
    if customer_order:
        return customer_order_schema.dump(customer_order)
    else:
        return {"error": f"Customer Order with id {customer_order_id} not found"}, 404
## requires authentication
# from datetime import date
# import functools

# from flask import Blueprint, request
# from flask_jwt_extended import jwt_required, get_jwt_identity

# from init import db
# from models.customer_order import Customer_Order, customer_orders_schema, customer_order_schema
# from models.customer import Customer
# #from controllers.comment_controller import comments_bp

# customer_orders_bp = Blueprint('custom_orders', __name__, url_prefix='/customer_orders')
# customer_orders_bp.register_blueprint(comments_bp) # TODO FIX THIS

# #TODO
# def authorise_as_admin(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
#         stmt = db.select(Customer).filter_by(id=user_id)
#         user = db.session.scalar(stmt)
#         # if the user is an admin
#         if user.is_admin:
#             # we will contine and will run the decorated function
#             return fn(*args, **kwargs)
#         # else (if the user is NOT an admin)
#         else:
#             # return an error
#             return {"error": "Not authorised to delete a customer order"}, 403
          
#     return wrapper

# #COMPLETE
# # http://localhost:8080/customer_orders - GET
# @customer_orders_bp.route('/')
# def get_all_custom_orders():
#     stmt = db.select(Customer_Order).order_by(Customer_Order.date.desc())
#     customer_orders = db.session.scalars(stmt)
#     return customer_orders_schema.dump(customer_orders)

# #COMPLETE
# # http://localhost:8080/customer_orders/1 - GET
# @customer_orders_bp.route('/<int:customer_order_id>')
# def get_one_customer_order(customer_order_id): # customer_order_id = 1
#     stmt = db.select(Customer_Order).filter_by(id=customer_order_id) # select * from customer_orders where id=1
#     customer_order = db.session.scalar(stmt)
#     if customer_order:
#         return customer_order_schema.dump(customer_order)
#     else:
#         return {"error": f"Customer_Order with id {customer_order_id} not found"}, 404
    

# # http://localhost:8080/customer_orders - POST
# @customer_orders_bp.route('/', methods=["POST"])
# @jwt_required()
# def create_customer_order():
#     body_data = customer_order_schema.load(request.get_json())
#     # Create a new customer_order model instance
#     customer_order = Customer_Order( 
        
#         #TODO FIX THESE VALUES
#         title = body_data.get('title'),
#         description = body_data.get('description'),
#         date = date.today(),
#         status = body_data.get('status'),
#         priority = body_data.get('priority'),
#         user_id = get_jwt_identity()
#     )

#     # id = db.Column(db.Integer, primary_key=True)
#     # location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
#     # customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
#     # vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
#     # #location_billing_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
#     # #sales_employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
#     # #sales_location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
#     # date_created = db.Column(db.Date)
#     # date_delivered = db.Column(db.Date)
#     # status = db.Column(db.String)
    
#     # location = db.relationship('Location', back_populates='customer_orders')
#     # customer = db.relationship('Customer', back_populates='customer_orders') #Customer can have multiple orders
#     # vehicle = db.relationship('Vehicle', back_populates='customer_order') #Only 1 order per vehicle
#     # #employee = db.relationship('Employee', back_populates='customer_order', uselist=False)





#     # Add that to the session and commit
#     db.session.add(customer_order)
#     db.session.commit()
#     # return the newly created customer_order
#     return customer_order_schema.dump(customer_order), 201





# # https://localhost:8080/customer_orders/6 - DELETE
# @customer_orders_bp.route('/<int:customer_order_id>', methods=["DELETE"])
# @jwt_required() # must be before as used inside authorise_as_admin
# @authorise_as_admin
# def delete_customer_order(customer_order_id):
#     # # check user's admin status
#     # is_admin = is_user_admin()
#     # if not is_admin:
#     #     return {"error": "Not authorised to delete a customer_order"}, 403
#     # get the customer_order from the db with id = customer_order_id
#     stmt = db.select(Customer_Order).where(Customer_Order.id == customer_order_id)
#     customer_order = db.session.scalar(stmt)
#     # if customer_order exists
#     if customer_order:
#         # delete the customer_order from the session and commit
#         db.session.delete(customer_order)
#         db.session.commit()
#         # return msg
#         return {'message': f"Customer_Order '{customer_order.title}' deleted successfully"}
#     # else
#     else:
#         # return error msg
#         return {'error': f"Customer_Order with id {customer_order_id} not found"}, 404
    
# # http://localhost:8080/customer_orders/5 - PUT, PATCH
# @customer_orders_bp.route('/<int:customer_order_id>', methods=["PUT", "PATCH"])
# @jwt_required()
# def update_customer_order(customer_order_id):
#     # Get the data to be updated from the body of the request
#     body_data = customer_order_schema.load(request.get_json(), partial=True)
#     # get the customer_order from the db whose fields need to be updated
#     stmt = db.select(Customer_Order).filter_by(id=customer_order_id)
#     customer_order = db.session.scalar(stmt)
#     # if customer_order exists
#     if customer_order:
#         if str(customer_order.user_id) != get_jwt_identity(): # Integer Field Vs String Field
#             return {"error": "Only the owner can edit the customer_order"}, 403
#         # update the fields
#         customer_order.title = body_data.get('title') or customer_order.title
#         customer_order.description = body_data.get('description') or customer_order.description
#         customer_order.status = body_data.get('status') or customer_order.status
#         customer_order.priority = body_data.get('priority') or customer_order.priority
#         # commit the changes
#         db.session.commit()
#         # return the updated customer_order back
#         return customer_order_schema.dump(customer_order)
#     # else
#     else:
#         # return error msg
#         return {'error': f'Customer_Order with id {customer_order_id} not found'}, 404
    

# def is_user_admin():
#     user_id = get_jwt_identity()
#     stmt = db.select(Customer).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     return user.is_admin


