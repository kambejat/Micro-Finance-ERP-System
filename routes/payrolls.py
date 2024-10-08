import datetime
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, marshal_with, marshal, fields
from models import db, Payroll

payroll_bp = Blueprint('payroll', __name__)

api = Api(payroll_bp)

payroll_parser = reqparse.RequestParser()

payroll_parser.add_argument('employee_id', type=int, default=None, help="Required employee identifier for employee")
payroll_parser.add_argument('date', type=datetime.datetime, default=None, help="Required date for employee")
payroll_parser.add_argument('gross_salary', type=float, default=None, help="Required amount of gross salary for employee")
payroll_parser.add_argument('deductions', type=float, default=None, help="Required amount of deduction to be paid for employee")
payroll_parser.add_argument('net_salary', type=float, default=None, help="Required a percentage of the total amount for employee to be paid for employee")
payroll_parser.add_argument('payment_method', type=str, default=None, help="Required a payment method")

payroll_fields = {
    'payroll_id': fields.Integer,
    'employee_id': fields.Integer,
    'date': fields.DateTime,
    'gross_salary': fields.Float,
    'deductions': fields.Float,
    'net_salary': fields.Float,
    'payment_method': fields.String
}

class PayrollResource(Resource):
    @marshal_with(payroll_fields)
    def get(self, payroll_id=None):
        if payroll_id:
            payroll = Payroll.query.get_or_404(payroll_id)
            return jsonify(payroll)
        payrolls = Payroll.query.all()
        return jsonify(payrolls)        
    
    @marshal_with(payroll_fields)
    def put(self, payroll_id):
        payroll = Payroll.query.get_or_404(payroll_id)
        data = payroll_parser.parse_args()
        for key, value in data.items():
            setattr(payroll, key, value)
        db.session.commit()
        return payroll
    
    def delete(self, payroll_id):
        payroll = Payroll.query.get_or_404(payroll_id)
        db.session.delete(payroll)
        db.session.commit()
        return jsonify({'message': 'Payroll deleted successfully'})
    
    @marshal_with(payroll_fields)
    def post(self):
        data = payroll_parser.parse_args()
        payroll = Payroll(**data)
        db.session.add(payroll)
        db.session.commit()
        return payroll, 201
    
    @marshal_with(payroll_fields)
    def patch(self, payroll_id):
        payroll = Payroll.query.get_or_404(payroll_id)
        data = payroll_parser.parse_args()
        for key, value in data.items():
            if value is not None:
                setattr(payroll, key, value)
        db.session.commit()
        return payroll
    

    def options(self):
        return {}, 200, {'Allow': 'GET, POST, PUT, DELETE, PATCH, OPTIONS'}

api.add_resource(PayrollResource, '/payrolls/<int:payroll_id>', '/payrolls')
payroll_bp.add_url_rule('/payrolls', view_func=PayrollResource.as_view('payrolls'))