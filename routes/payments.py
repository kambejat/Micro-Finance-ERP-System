import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from models import db, Payment

payments_bp = Blueprint('payments', __name__)

api = Api(payments_bp)

payment_parser = reqparse.RequestParser()

payment_parser.add_argument('payment_id', type=int, default=True, help="Required payment identifier")
payment_parser.add_argument('loan_id', type=int, default=None, help="Required loan identifier")
payment_parser.add_argument('date', type=datetime.datetime, default=None, help="Date of interest to be paid")
payment_parser.add_argument('amount', type=float, default=None, help="Amount to be paid to the customer")
payment_parser.add_argument('payment_method', type=str, default=None, help="Payment method to be used for the customer to pay")

payment_fields = {
    'payment_id': fields.Integer,
    'loan_id': fields.Integer,
    'date': fields.DateTime,
    'amount': fields.Float,
    'payment_method': fields.String
}

class PaymentResource(Resource):
    @marshal_with(payment_fields)
    def get(self, payment_id=None):
        if payment_id:
            payment = Payment.query.get_or_404(payment_id)
            return payment
        else:
            payments = Payment.query.all()
            return {'payments': [marshal(payment, payment_fields) for payment in payments]}
    
    @marshal_with(payment_fields)
    def post(self):
        data = payment_parser.parse_args()
        new_payment = Payment(
            loan_id=data['loan_id'],
            date=data['date'],
            amount=data['amount'],
            payment_method=data['payment_method']
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment, 201
    
    @marshal_with(payment_fields)
    def put(self, payment_id):
        data = payment_parser.parse_args()
        payment = Payment.query.get_or_404(payment_id)
        payment.loan_id = data['loan_id']
        payment.date = data['date']
        payment.amount = data['amount']
        payment.payment_method = data['payment_method']
        db.session.commit()
        return payment, 200
    
    def delete(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return {'message': 'Payment deleted successfully'}, 200
    
    @marshal_with(payment_fields)
    def patch(self, payment_id):
        data = payment_parser.parse_args()
        payment = Payment.query.get_or_404(payment_id)
        if 'loan_id' in data:
            payment.loan_id = data['loan_id']
        if 'date' in data:
            payment.date = data['date']
        if 'amount' in data:
            payment.amount = data['amount']
        if 'payment_method' in data:
            payment.payment_method = data['payment_method']
        db.session.commit()
        return payment, 200
    

api.add_resource(PaymentResource, '/payments', '/payments/<int:payment_id>')
payments_bp.add_url_rule('/payments', view_func=PaymentResource.as_view('payments'))