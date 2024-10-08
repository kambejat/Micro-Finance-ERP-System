import datetime
from flask import Blueprint, json, request

from flask_restful import Api, Resource, reqparse, fields, marshal_with

from models import db, Loan

loans_bp = Blueprint('loans', __name__)

api = Api(loans_bp)

loan_parser = reqparse.RequestParser()

loan_parser.add_argument('customer_id', type=int, required=True, help="Customer ID is required")
loan_parser.add_argument('account_id', type=int, required=True, help="Account ID is required")
loan_parser.add_argument('loan_type', type=str, required=True, help="Account type is required")
loan_parser.add_argument('amount', type=float, required=True, help="Loan amount is required")
loan_parser.add_argument('interest_rate', type=float, required=True, help="Interest rate is required")
loan_parser.add_argument('term_years', type=int, required=True, help="Term years is required")
loan_parser.add_argument('start_date', type=datetime, required=True, help="Start date is required")
loan_parser.add_argument('end_date', type=datetime, required=True, help="End date is required")
loan_parser.add_argument("status", type=str, required=True , help="Status is required when creating account or updating account")

loans_fields = {
    'loan_id': fields.Integer,
    'customer_id': fields.Integer,
    'account_id': fields.Integer,
    'loan_type': fields.String,
    'amount': fields.Float,
    'interest_rate': fields.Float,
    'term_years': fields.Integer,
    'start_date': fields.DateTime(dt_format='iso8601'),
    'end_date': fields.DateTime(dt_format='iso8601'),
    'status': fields.String
}

class LoanResource(Resource):
    @marshal_with(loans_fields)
    def get(self, loan_id):
        loan = Loan.query.get_or_404(loan_id)
        return loan
    
    @marshal_with(loans_fields)
    def put(self, loan_id):
        data = loan_parser.parse_args()
        loan = Loan.query.get_or_404(loan_id)
        loan.customer_id = data.get('customer_id')
        loan.account_id = data.get('account_id')
        loan.loan_type = data.get('loan_type')
        loan.amount = data.get('amount')
        loan.interest_rate = data.get('interest_rate')
        loan.term_years = data.get('term_years')
        loan.start_date = data.get('start_date')
        loan.status = data.get('status')
        db.session.commit()
        return loan
    
    @marshal_with(loans_fields)
    def delete(self, loan_id):
        loan = Loan.query.get_or_404(loan_id)
        db.session.delete(loan)
        db.session.commit()
        return {'message': 'Loan deleted successfully'}, 200
    
    @marshal_with(loans_fields)
    def post(self):
        data = loan_parser.parse_args()
        loan = Loan(
            customer_id=data.get('customer_id'),
            account_id=data.get('account_id'),
            loan_type=data.get('loan_type'),
            amount=data.get('amount'),
            interest_rate=data.get('interest_rate'),
            term_years=data.get('term_years'),
            start_date=data.get('start_date'),
            status=data.get('status')
        )
        db.session.add(loan)
        db.session.commit()
        return loan, 201
    
    def calculate_end_date(self, loan):
        end_date = loan.start_date + datetime.timedelta(days=loan.term_years * 365)
        return end_date
    
    def calculate_loan_status(self, loan):
        today = datetime.date.today()
        if today >= loan.end_date:
            return 'Expired'
        elif today >= loan.start_date:
            return 'Active'
        else:
            return 'Pending'
    
    def update_loan(self, loan):
        loan.end_date = self.calculate_end_date(loan)
        loan.status = self.calculate_loan_status(loan)
        db.session.commit()
        return loan

api.add_resource(LoanResource, '/loans/<int:loan_id>', endpoint='loan')
api.add_resource(LoanResource, '/loans', endpoint='loans')

        
    