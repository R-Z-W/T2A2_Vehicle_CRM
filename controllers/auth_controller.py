#TODO REVIEW

from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.customer import Customer, customer_schema
from models.employee import Employee, employee_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/register", methods=["POST"]) # /auth/register
def auth_register():
    try:
        # the data that we get in body of the request
        body_data = request.get_json()

        # create the customer instance
        customer = Customer(
            fname=body_data.get('fname'),
            email=body_data.get('email')
        )

        # password from the request body
        password = body_data.get('password')
        # if password exists, hash the password
        if password:
            customer.password = bcrypt.generate_password_hash(password).decode('utf-8')

        # add and commit the customer to DB
        db.session.add(customer)
        db.session.commit()
        # Repond back to the client
        return customer_schema.dump(customer), 201

    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # 23503
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # 23505
            return {"error": "Email address already in use"}, 409


@auth_bp.route("/login", methods=["POST"]) # /auth/login
def auth_login():
    # get the data from the request body
    body_data = request.get_json()
    # Find the customer with the email address
    stmt = db.select(Customer).filter_by(email=body_data.get("email"))
    customer = db.session.scalar(stmt)
    # If customer exists and password is correct
    if customer and bcrypt.check_password_hash(customer.password, body_data.get("password")):
        # create jwt
        token = create_access_token(identity=str(customer.id), expires_delta=timedelta(days=1))
        # return the token along with the customer info
        return {"email": customer.email, "token": token, "is_admin": customer.is_admin}
    # else
    else:
        # return error
        return {"error": "Invalid email or password"}, 401