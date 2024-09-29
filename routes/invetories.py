import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from models import db
from models import InventoryItem as Inventory

inventory_bp = Blueprint('inventory', __name__)
api = Api(inventory_bp)

inventory_parser = reqparse.RequestParser()

inventory_parser.add_argument('item_id', type=int, default=True, help="Required item identifier")
inventory_parser.add_argument('name', type=str, default=None, help="Name of the inventory item")
inventory_parser.add_argument('description', type=str, default=None, help="Description of the inventory item")
inventory_parser.add_argument('quantity', type=int, default=None, help="Quantity of the inventory item")
inventory_parser.add_argument('unit_price', type=float, default=None, help="Quantity of the inventory item")
inventory_parser.add_argument('category_id', type=int, default=None, help="Id of the inventory category")
inventory_parser.add_argument('brand_id', type=int, default=None, help="Id of the inventory brand")
inventory_parser.add_argument('created_at', type=datetime.datetime, default=None, help="Date when the inventory item was created")

inventory_fields = {
    'item_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'quantity': fields.Integer,
    'unit_price': fields.Float,
    'category_id': fields.Integer,
    'brand_id': fields.Integer,
    'created_at': fields.DateTime
}

class InventoryResource(Resource):
    @marshal_with(inventory_fields)
    def get(self, item_id=None):
        if item_id:
            item = Inventory.query.get_or_404(item_id)
            return item
        items = Inventory.query.all()
        return jsonify(items)
    
    @marshal_with(inventory_fields)
    def post(self):
        data = inventory_parser.parse_args()
        item = Inventory(
            item_id=data['item_id'],
            name=data['name'],
            description=data['description'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            category_id=data['category_id'],
            brand_id=data['brand_id'],
            created_at=datetime.datetime.now()
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item), 201
    
    @marshal_with(inventory_fields)
    def put(self, item_id):
        data = inventory_parser.parse_args()
        item = Inventory.query.get_or_404(item_id)
        item.name = data.get('name')
        item.description = data.get('description')
        item.quantity = data.get('quantity')
        item.unit_price = data.get('unit_price')
        item.category_id = data.get('category_id')
        item.brand_id = data.get('brand_id')
        db.session.commit()
        return jsonify(item), 200
    
    def delete(self, item_id):
        item = Inventory.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Inventory item deleted successfully'}, 200
    
    def patch(self, item):
        data = request.get_json()
        if 'quantity' in data:
            item.quantity += data['quantity']
        if 'name' in data:
            item.name = data['name']
        db.session.commit()
        return jsonify(item), 200

api.add_resource(InventoryResource, '/inventory', '/inventory/<int:item_id>')
inventory_bp.add_url_rule('/inventory', view_func=InventoryResource.as_view('inventory'))