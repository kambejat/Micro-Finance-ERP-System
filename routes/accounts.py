import datetime
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, Account


accounts_bp = Blueprint('accounts', __name__)
api = Api(accounts_bp)

account_parser = reqparse.RequestParser()
account_parser.add_argument('account_id', type=int, default=True, help="Required account identifier")
account_parser.add_argument('customer_id', type=int, default=None, help='Customer identifier for the account')
account_parser.add_argument('account_number', type=str, required=True, help='Account number is required')
account_parser.add_argument('account_type', type=str, required=True, help='Account type is required')
account_parser.add_argument('balance', type=float, required=True, help='Balance amount')
account_parser.add_argument('opened_at', type=datetime.datetime, required=False, help='')
account_parser.add_argument('status', type=str, required=True, help='Account status', default='Active')

accounts_fields = {
    'account_id': fields.Integer,
    'customer_id': fields.Integer,
    'account_number': fields.String,
    'account_type': fields.String,
    'balance': fields.Float,
    'opened_at': fields.DateTime(dt_format='iso8601'),
}

class AccountResource(Resource):
    def get(self, account_id=None):
        if account_id:
            account = Account.query.get_or_404(account_id)
            return jsonify({
                "account_id": account.account_id,
                "account_number": account.account_number,
                "account_type": account.account_type,
                "balance": account.balance,
                "customer_id": account.customer_id,
                "status": account.status
            })
        accounts = Account.query.all()
        return jsonify([{
            "account_id": account.account_id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": account.balance,
            "customer_id": account.customer_id,
            "status": account.status
        } for account in accounts])

    def post(self):
        data = request.get_json()
        new_account = Account(
            customer_id=data['customer_id'],
            account_number=data['account_number'],
            account_type=data['account_type'],
            balance=data['balance']
        )
        db.session.add(new_account)
        db.session.commit()
        return jsonify({"message": "Account created successfully", "account_id": new_account.account_id})

    def put(self, account_id):
        data = request.get_json()
        account = Account.query.get_or_404(account_id)
        account.account_number = data['account_number']
        account.account_type = data['account_type']
        account.balance = data['balance']
        account.status = data['status']
        db.session.commit()
        return jsonify({"message": "Account updated successfully"})

    def delete(self, account_id):
        account = Account.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"})
    

api.add_resource(AccountResource, '/accounts')
