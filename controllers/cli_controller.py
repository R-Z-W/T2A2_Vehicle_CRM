from datetime import date
from flask import Blueprint
from init import db, bcrypt

from models.location import Location
from models.bank import Bank
from models.vehicle import Vehicle
from models.employee import Employee
from models.customer import Customer
from models.customer_order import Customer_Order
from models.workorder import Workorder
from models.workorder_comment import Workorder_Comment

# Terminal commands start as: flask db ...
db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('seed')
def seed_tables():

    locations = [
        Location(
            address1 = "17 George Street",
            city = "Sydney",
            postal_code = 2000,
            state = "NSW",
            country = "Australia"
        ),
        Location(
            address1 = "13 Park Lane",
            city = "Perth",
            postal_code = 3213,
            state = "WA",
            country = "Australia"
        ),
        Location(
            address1 = "101 King Street",
            address2 = "U10",
            city = "Melbourne",
            postal_code = 2343,
            state = "Victoria",
            country = "Australia"
        )
        ]
    db.session.add_all(locations)

    banks = [
        Bank(
            account_name="Customer1",
            account_num=5738291610348752,
            account_bsb=123456,
            bank_name="Big Bank",
            date_created=date.today()
        ),
        Bank(
            account_name="Customer2",
            account_num=5738291610348752,
            account_bsb=123456,
            bank_name="Big Bank",
            date_created=date.today()
        ),
        Bank(
            account_name="Customer3",
            account_num=5738291610348752,
            account_bsb=123456,
            bank_name="Big Bank",
            date_created=date.today()
        )
    ]
    db.session.add_all(banks)
    
    vehicles = [
        # TODO DELETE ADMIN ABILITY ALSO IN model
        # Admin Customer
        Vehicle(
            vin="JH4DC4450RS000102",
            model_name="RAV4",
            model_manufacturer="Toyota",
            model_price=30000,
            location=locations[1]
        ),
        Vehicle(
            vin="6TXXU2R38D6A29783",
            model_name="Everest",
            model_manufacturer="Ford",
            model_price=45000,
            location=locations[1]
        ),
        Vehicle(
            vin="5YJ3E1EB9KF619084",
            model_name="CX9",
            model_manufacturer="Mazda",
            model_price=38000,
            location=locations[1]
        )
    ]
    db.session.add_all(vehicles)

    employees = [
        Employee(
            role="Mechanic",
            work_department="Mechanic Shop"
        ),
        Employee(
            role="Sales",
            work_department="Office"
        ),
        Employee(
            role="Delivery",
            work_department="Front Of House"
        )
    ]
    db.session.add_all(employees)

    customers = [
        # Admin Customer
        Customer(
            email="admin@email.com",
            licence_num="5839124",
            location=locations[0],
            bank=banks[0],
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        Customer(
            fname="CustomerFirst1",
            lname="CustomerLast1",
            email="Customer1@email.com",
            licence_num="7294851",
            location=locations[1],
            bank=banks[1],
            employee=employees[0],
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        Customer(
            fname="CustomerFirst2",
            lname="CustomerLast2",
            email="Customer2@email.com",
            licence_num="2314823",
            location=locations[2],
            bank=banks[2],
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]
    db.session.add_all(customers)

    workorders = [
        Workorder(
            employee=employees[1],
            vehicle=vehicles[0],
            status="Available",
            title="Broken Fender",
            description="Fix: Replace rear fender",
            date_created=date.today()
            ),
        Workorder(
            employee=employees[1],
            vehicle=vehicles[0],
            status="Available",
            title="Detail Car",
            description="Please Clean",
            date_created=date.today(),
            date_completed=date.today()
            )
    ]
    db.session.add_all(workorders)

    customer_orders = [
        Customer_Order(
            location=locations[1],
            customer=customers[0],
            vehicle=vehicles[1],
            date_created=date.today(),
            date_delivered=date.today()
        ),
        Customer_Order(
            location=locations[0],
            customer=customers[0],
            vehicle=vehicles[0],
            date_created=date.today(),
            date_delivered=date.today()
        )
    ]
    db.session.add_all(customer_orders)

    workorder_comments = [
        Workorder_Comment(
            workorder=workorders[0],
            employee=employees[0],
            title="Request Part",
            message="Part not in stock, coming in 2 weeks",
            date_created=date.today()
        ),
        Workorder_Comment(
            workorder=workorders[1],
            employee=employees[1],
            title="Damage Alert",
            message="Damage found during detailing. Creating new WO",
            date_created=date.today()
        )
    ]
    db.session.add_all(workorder_comments)

    db.session.commit()
    print("Tables Seeded")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables Dropped")