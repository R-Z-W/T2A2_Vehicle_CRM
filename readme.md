<h1>Installation</h1>

1. Install postgresql if not already installed
2. Open a terminal and type ```sudo -u postgres psql```
3. Create database called: vehicle_db: ```CREATE DATABASE vehicles_db;```
4. Enter the database with ```\c vehicles_db``` and create a user called db_manager with a password: ```CREATE USER db_manager WITH PASSWORD '123456';```
5. Create priviliges to user: ```GRANT ALL PRIVILEGES ON DATABASE vehicles_db TO db_manager;```
6. If postgres permission denied for schema public. Input into terminal: ```GRANT ALL ON SCHEMA public TO db_manager;```
<br/><br/>

7. Once the the PostgreSQL database has been made set up, make sure python 3.10 or above is installed.
8. Check by typing in the terminal ```python -version```. If not installed or below 3.10, install python from python.org
9. Download contents from this repo.
10. Open a terminal in this repo.
11. Activate the virtual environment by typing ```source .venv/bin/activate``` in the terminal.
12. Install requirements ```pip install -r requirements.txt```
13. Type ```flask db create``` to create tables.
14. Type ```flask db seed``` to seed tables.
15. Type ```flask db drop``` to drop tables to remove tables.
* Extra step: Enter postgresql again: ```sudo -u postgres psql```. Type ```DROP DATABASE vehicle_db;``` to remove database and ```DROP USER db_manager;``` to remove user.


<h2>R1 Identification of the problem you are trying to solve by building this particular app.</h2>
With the advent of Covid-19, disrupting supply chains of newly manufactured automobiles and the rising costs of living effecting people’s budgets, the rise of purchasing a second-hand car has become more popular than ever. Due to this, a new disruptive industry of online car dealerships has emerged to capitalise on this opportunity. This app aims to support this industry by providing a package that tracks the vehicle reconditioning process and offers a platform to store information on vehicle inventory, which subsequentially can be readily accessed by customers upon request.

<h2>R2  Why is it a problem that needs solving?</h2>
As costs rise for customers with increased interest rates and inflation, and the disruptions to supply chains further decreasing inventory of vehicles in Australia, the cost of purchasing a new vehicle is financially unattainable for many Australians. Thus, the alternative of purchasing a second-hand car has become a more viable option for many Australians. But in-order to effectively compete in the second-hand market, ways of reducing cost in all aspects of the business need to be considered. By not being constrained by the limitations of physical space, or day to day operations of a traditional walk-in dealership, online car dealerships can set up operations on inexpensive land for the accumulation of a vast inventory of vehicles at a low cost. However, managing such a vast inventory presents challenges, particularly in terms of inventory tracking and presentation to customers. Thus, the aim of this API is to address these challenges and provide solutions for efficient inventory management and display in the online car dealership industry.

<h2>R3	Why have you chosen this database system. What are the drawbacks compared to others?</h2>
I have chosen PostgreSQL as my database system because it is a relational database, making it easy to establishing connections between vehicles and customers, as well as managing relationships between work orders and employees. This database allows for simple data management and retrieval processes and has robust security mechanisms, providing the flexibility and functionality required for my project.

However, PostgreSQL does have its drawbacks compared to other database systems. One such drawback is its comparatively slower performance with large datasets when contrasted with alternatives like MongoDB (non-relational database) or TimescaleDB (relational database). Additionally, PostgreSQL may not match the performance capabilities of distributed database systems, such as Apache Cassandra and Google Cloud Spanner, when it comes to handling high levels of traffic from website visits and/or workorder queries.

<h2>R4	Identify and discuss the key functionalities and benefits of an ORM</h2>
Object-Relational Mapping (ORM) allows for the connection between an object oriented programming language and a relational database. An example of an ORM is SQLAlchemy, a python library which serves as way to interact with the database using the python language. SQLAlchemy achieves this by defining models which are python classes. These models provide the ability to not only perform CRUD operations such as create, read, update and delete, but also uphold data integrity with data validation and a range of data relationships.

<h2>R5	Document all endpoints for your API</h2>

- http://localhost:8080/banks
- http://localhost:8080/banks/{id}

- http://localhost:8080/customers
- http://localhost:8080/customers/{id}

- http://localhost:8080/customer_orders
- http://localhost:8080/customers_orders/{id}

- http://localhost:8080/locations
- http://localhost:8080/locations/{id}

- http://localhost:8080/workorders
- http://localhost:8080/workorders/{id}

- http://localhost:8080/vehicles
- http://localhost:8080/vehicles/{id}

- http://localhost:8080/employees
- http://localhost:8080/employees/{id}

- http://localhost:8080/locations
- http://localhost:8080/locations/{id}

<h2>R6	An ERD for your app</h2>

![VehicleCRM_ERM](./imgs/vehiclecrm.png)

R7	Detail any third party services that your app will use</h2>
- SQLAlchemy:
SQLAlchemy is a Python library that acts as an object-relational mapping (ORM) tool. It enables interaction with the API's database without the necessity of using direct SQL queries. By defining models as Python classes, SQLAlchemy facilitates tasks such as table creation, population, modification, and deletion within the database. It also supports 

- Marshmallow:
Marshmallow is a Python library designed for the serialization and deserialization of data within the API. It allows for the conversion of complex data types, such as Python objects, to and from formats like JSON which is suitable for transmission over networks. Marshmallow employs schemas containing fields that define the structure of data during serialization or deserialization. These fields may include validation rules to ensure that the data meets specified criteria, ensuring data integrity and consistency in the API.

- JWT (Bearer):
JSON Web Tokens (JWT) is used for customer identification within the API. JWT generates a token from customer information that uniquely identifies the customer without the need to store their session information.

<h2>R8	Describe your projects models in terms of the relationships they have with each other</h2>


<h2>R9	Discuss the database relations to be implemented in your application</h2>


<h2>R10	Describe the way tasks are allocated and tracked in your project</h2>