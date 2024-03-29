#requires authentication

from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.bank import Bank, banks_schema, bank_schema

banks_bp = Blueprint('banks', __name__, url_prefix='/banks')

#TODO ONLY USER WITH ID OR ADMIN CAN GET POST PATCH DELETE

# GET ALL BANKS
# http://localhost:8080/banks - GET
@banks_bp.route('/')
def get_all_banks():
    stmt = db.select(Bank).order_by(Bank.date_created.desc())
    banks = db.session.scalars(stmt)
    return banks_schema.dump(banks)

# GET BANK VIA ID
# http://localhost:8080/banks/*id - GET
@banks_bp.route('/<int:bank_id>')
def get_one_bank(bank_id): # bank_id = *id
    stmt = db.select(Bank).filter_by(id=bank_id) # select * from banks where id=*id
    bank = db.session.scalar(stmt)
    if bank:
        return bank_schema.dump(bank)
    else:
        return {"error": f"Bank with id {bank_id} not found"}, 404
    

@banks_bp.route("/", methods=["POST"])
# @jwt_required()
def create_bank():
    body_data = bank_schema.load(request.get_json())
    # Create a new bank model instance
    bank = Bank(
        account_name = body_data.get('account_name'),
        account_num = body_data.get('account_num'),
        account_bsb = body_data.get('account_bsb'),
        bank_name = body_data.get('bank_name'),
        date_created = date.today()
    )
    # Add that to the session and commit
    db.session.add(bank)
    db.session.commit()
    # return the newly created bank
    return bank_schema.dump(bank), 201

@banks_bp.route('/<int:bank_id>', methods=["DELETE"])
def delete_bank(bank_id):
    stmt = db.select(Bank).where(Bank.id == bank_id)
    bank = db.session.scalar(stmt)
    # if bank exists
    if bank:
        # delete the bank from the session and commit
        db.session.delete(bank)
        db.session.commit()
        # return msg
        return {'message': f"Bank '{bank.id}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Bank with id {bank_id} not found"}, 404
    

# http://localhost:8080/banks/5 - PUT, PATCH
@banks_bp.route('/<int:bank_id>', methods=["PUT", "PATCH"])
def update_bank(bank_id):
    # Get the data to be updated from the body of the request
    body_data = bank_schema.load(request.get_json(), partial=True)
    # Get the bank from the db whose fields need to be updated
    stmt = db.select(Bank).filter_by(id=bank_id)
    bank = db.session.scalar(stmt)
    # if bank exists
    if bank:
        # if str(bank.user_id) != get_jwt_identity(): # Integer Field Vs String Field
        #     return {"error": "Only the owner can edit the bank"}, 403
        # # update the fields
        bank.account_name = body_data.get('account_name') or bank.account_name
        bank.account_num = body_data.get('account_num') or bank.account_num
        bank.account_bsb = body_data.get('account_bsb') or bank.account_bsb
        bank.bank_name = body_data.get('bank_name') or bank.bank_name
        # commit the changes
        db.session.commit()
        # return the updated bank back
         
        return bank_schema.dump(bank)

    # else
    else:
        # return error msg
        return {'error': f'Bank with id {bank_id} not found'}, 404