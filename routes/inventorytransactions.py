import datetime
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from models import db, InventoryTransaction

inventory_transactions_bp = Blueprint('inventory_transactions', __name__)
api = Api(inventory_transactions_bp)

inventory_transaction_parser = reqparse.RequestParser()

inventory_transaction_parser.add_argument('transaction_id', type=int, default=True, help="Required inventory transaction identifier")
inventory_transaction_parser.add_argument('item_id', type=str, default=None, help="Required inventory item identifier") 
inventory_transaction_parser.add_argument('date', type=datetime, default=None, help="Date of inventory transaction")
inventory_transaction_parser.add_argument('quantity', type=int, default=None, help="Quantity of inventory transaction")
inventory_transaction_parser.add_argument('transaction_type', type=str, default=None, help="Type of inventory transaction")
inventory_transaction_parser.add_argument('description', type=str, default=None, help="Description of inventory transaction")
inventory_transaction_parser.add_argument('branch_id', type=str, default=None, help="Branch ID of inventory transaction")

inventory_transactions_fields = {
    'transaction_id': fields.Integer,
    'item_id': fields.String,
    'date': fields.DateTime,
    'quantity': fields.Integer,
    'transaction_type': fields.String,
    'description': fields.String,
    'branch_id': fields.String
}

class InventoryTransactionsResource(Resource):
    @marshal_with(inventory_transactions_fields)
    def get(self):
        transactions = InventoryTransaction.query.all()
        return transactions
    
    @marshal_with(inventory_transactions_fields)
    def post(self):
        data = inventory_transaction_parser.parse_args()
        transaction = InventoryTransaction(transaction_id=data['transaction_id'], item_id=data['item_id'], date=data['date'], quantity=data['quantity'], transaction_type=data['transaction_type'], description=data['description'], branch_id=data['branch_id'])
        db.session.add(transaction)
        db.session.commit()
        return transaction, 201
    
    @marshal_with(inventory_transactions_fields)
    def put(self, transaction_id):
        data = inventory_transaction_parser.parse_args()
        transaction = InventoryTransaction.query.get_or_404(transaction_id)
        transaction.item_id = data['item_id']
        transaction.date = data['date']
        transaction.quantity = data['quantity']
        transaction.transaction_type = data['transaction_type']
        transaction.description = data['description']
        transaction.branch_id = data['branch_id']
        db.session.commit()
        return transaction, 200
    
    def delete(self, transaction_id):
        transaction = InventoryTransaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return {'message': 'Inventory transaction deleted successfully'}, 200
    
    def patch(self, transaction_id):
        data = inventory_transaction_parser.parse_args()
        transaction = InventoryTransaction.query.get_or_404(transaction_id)
        if 'item_id' in data:
            transaction.item_id = data['item_id']
        if 'date' in data:
            transaction.date = data['date']
        if 'quantity' in data:
            transaction.quantity = data['quantity']
        if 'transaction_type' in data:
            transaction.transaction_type = data['transaction_type']
        if 'description' in data:
            transaction.description = data['description']
        if 'branch_id' in data:
            transaction.branch_id = data['branch_id']
        db.session.commit()
        return transaction, 200
    
    def options(self):
        return {}, 200


api.add_resource(InventoryTransactionsResource, '/inventory_transactions')
inventory_transactions_bp.add_url_rule('/inventory_transactions', view_func=InventoryTransactionsResource.as_view('inventory_transactions'))