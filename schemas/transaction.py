from flask_marshmallow import Marshmallow
from models import Transaction

ma = Marshmallow()

class TransactionSchema(ma.Schema):
    class Meta:
        model = Transaction
        load_instance = True


transaction_schema = TransactionSchema()
transaction_schemas = TransactionSchema(many=True)