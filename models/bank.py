from init import db, ma
from marshmallow import fields

class Bank(db.Model):
    __tablename__ = "banks"

    id  = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String)
    account_num = db.Column(db.BigInteger)
    account_bsb = db.Column(db.Integer)
    bank_name = db.Column(db.String)
    date_created = db.Column(db.Date, nullable=False)

    customers = db.relationship('Customer', back_populates='bank')

class BankSchema(ma.Schema):

    customers = fields.List(fields.Nested('CustomerSchema', exclude=['bank'])) # multi customer shared bank

    class Meta:
        fields = ('id', 'account_name', 'account_num', 'account_bsb', 'bank_name', 'date_created')

bank_schema = BankSchema()
banks_schema = BankSchema(many=True)