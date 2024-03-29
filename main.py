import os
from flask import Flask
from init import db, ma, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    # App Factories Flask

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    #connect libraries with flask app

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)




    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.bank_controller import banks_bp
    app.register_blueprint(banks_bp)

    from controllers.employee_controller import employees_bp
    app.register_blueprint(employees_bp)
    
    from controllers.location_controller import locations_bp
    app.register_blueprint(locations_bp)

    from controllers.vehicle_controller import vehicles_bp
    app.register_blueprint(vehicles_bp)

    from controllers.workorder_controller import workorders_bp
    app.register_blueprint(workorders_bp)

    from controllers.customer_controller import customers_bp
    app.register_blueprint(customers_bp)

    from controllers.customer_order_controller import customer_orders_bp
    app.register_blueprint(customer_orders_bp)



    return app