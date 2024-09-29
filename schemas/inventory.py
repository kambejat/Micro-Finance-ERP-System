from flask_marshmallow import Marshmallow
from models import InventoryItem

ma = Marshmallow()

class InventoryItemSchema(ma.Schema):
    class Meta:
        model = InventoryItem
        load_instance = True


inventory_item_schema = InventoryItemSchema()
inventory_item_list_schema = InventoryItemSchema(many=True)