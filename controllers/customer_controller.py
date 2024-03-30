#requires authentication


from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
# from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes


from init import db, bcrypt
from models.customer import Customer, customers_schema, customer_schema


customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# http://localhost:8080/customers - GET
@customers_bp.route('/')
def get_all_customers():
    stmt = db.select(Customer)
    customers = db.session.scalars(stmt)
    return customers_schema.dump(customers)

# http://localhost:8080/customers/*id - GET
@customers_bp.route('/<int:customer_id>')
def get_one_card(customer_id): # card_id = *id
    stmt = db.select(Customer).filter_by(id=customer_id) # select * from customers where id=*id
    customer = db.session.scalar(stmt)
    if customer:
        return customer_schema.dump(customer)
    else:
        return {"error": f"Customer with id {customer_id} not found"}, 404
    

@customers_bp.route("/", methods=["POST"])
# @jwt_required()
def register_customer():
    try:
        body_data = request.get_json()
        # Create a new customer model instance
        customer = Customer(
            fname = body_data.get('fname'),
            lname = body_data.get('lname'),
            gender = body_data.get('gender'),
            birth_date = body_data.get('birth_date'),
            email = body_data.get('email'),
            phone_num = body_data.get('phone_num'),
            licence_num = body_data.get('licence_num'),
            is_admin = body_data.get('is_admin'),
            bank_id = body_data.get('bank_id'),
            location_id = body_data.get('location_id'),
            employee_id = body_data.get('employee_id')
        )

        password = body_data.get('password')
        if password:
                customer.password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add that to the session and commit
        db.session.add(customer)
        db.session.commit()
        # return the newly created customer
        return customer_schema.dump(customer), 201
    
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # 23503
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # 23505
            return {"error": "Value already in use"}, 409
        

@customers_bp.route('/<int:customer_id>', methods=["DELETE"])
def delete_customer(customer_id):
    stmt = db.select(Customer).where(Customer.id == customer_id)
    customer = db.session.scalar(stmt)
    # if customer exists
    if customer:
        # delete the customer from the session and commit
        db.session.delete(customer)
        db.session.commit()
        # return msg
        return {'message': f"Customer '{customer.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Customer with id {customer_id} not found"}, 404
    

# http://localhost:8080/customers/5 - PUT, PATCH
@customers_bp.route('/<int:customer_id>', methods=["PUT", "PATCH"])
def update_customer(customer_id):
    # Get the data to be updated from the body of the request
    body_data = customer_schema.load(request.get_json(), partial=True)
    # Get the customer from the db whose fields need to be updated
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    # if customer exists
    if customer:

        customer.fname = body_data.get('fname') or customer.fname
        customer.lname = body_data.get('lname') or customer.lname
        customer.gender = body_data.get('gender')  or customer.gender
        customer.birth_date = body_data.get('birth_date') or customer.birth_date
        customer.email = body_data.get('email') or customer.email
        customer.phone_num = body_data.get('phone_num') or customer.phone_num
        customer.licence_num = body_data.get('licence_num') or customer.licence_num
        customer.password = body_data.get('password') or customer.password
        customer.is_admin = body_data.get('is_admin') or customer.is_admin
        customer.bank_id = body_data.get('bank_id') or customer.bank_id
        customer.location_id = body_data.get('location_id') or customer.location_id
        customer.employee_id = body_data.get('employee_id') or customer.employee_id 
        # commit the changes
        db.session.commit()
        # return the updated customer back
         
        return customer_schema.dump(customer)

    # else
    else:
        # return error msg
        return {'error': f'Customer with id {customer_id} not found'}, 404