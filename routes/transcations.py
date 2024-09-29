import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from models import db, Transaction

transactions_bp = Blueprint('transactions', __name__)

api = Api(transactions_bp)

transactions_parser = reqparse.RequestParser()
transactions_parser.add_argument('transaction_id', type=int, default=True, help="Required transaction identifier")
transactions_parser.add_argument("account_id", type=int, default=None, help="Account identifier is required")
transactions_parser.add_argument("date", type=datetime, default=None, help="Date to update transaction")
transactions_parser.add_argument("amount", type=float, default=None, help="Amount is required")
transactions_parser.add_argument("description", type=str, default=None, help="Description of transaction to update")
transactions_parser.add_argument("transaction_type", type=str, default=None, help="Type of transaction")

transaction_fields = {
    'transaction_id': fields.Integer,
    'account_id': fields.Integer,
    'date': fields.String,
    'amount': fields.Float,
    'description': fields.String,
    'transaction_type': fields.String
}

class TransactionResource(Resource):
    @marshal_with(transaction_fields)
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = Transaction.query.get_or_404(transaction_id)
            return transaction
        transactions = Transaction.query.all()
        return transactions
    
    @marshal_with(transaction_fields)
    def post(self):
        data = transactions_parser.parse_args()
        transaction = Transaction(account_id=data['account_id'], date=data['date'], amount=data['amount'], description=data['description'], transaction_type=data['transaction_type'])
        db.session.add(transaction)
        db.session.commit()
        return transaction, 201
    
    @marshal_with(transaction_fields)
    def put(self, transaction_id):
        data = transactions_parser.parse_args()
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.account_id = data.get('account_id')
        transaction.date = data.get('date')
        transaction.amount = data.get('amount')
        transaction.description = data.get('description')
        transaction.transaction_type = data.get('transaction_type')
        db.session.commit()
        return transaction, 200
    
    def delete(self, transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return {'message': 'Transaction deleted successfully'}, 200
    
    @marshal_with(transaction_fields)
    def patch(self, transaction_id):
        data = transactions_parser.parse_args()
        transaction = Transaction.query.get_or_404(transaction_id)
        if data.get('account_id'):
            transaction.account_id = data['account_id']
        if data.get('date'):
            transaction.date = data['date']
        if data.get('amount'):
            transaction.amount = data['amount']
        if data.get('description'):
            transaction.description = data['description']
        if data.get('transaction_type'):
            transaction.transaction_type = data['transaction_type']
        db.session.commit()
        return transaction, 200