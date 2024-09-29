from flask_marshmallow import Marshmallow
from models import InventoryTransaction

ma = Marshmallow()

class InventoryTransactionSchema(ma.Schema):
    class Meta:
        model = InventoryTransaction
        load_instance = True


inventory_transaction_schema = InventoryTransactionSchema()
inventory_transaction_list_schema =  InventoryTransactionSchema(many=True)