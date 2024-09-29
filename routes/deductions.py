from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, Deduction

deductions_bp = Blueprint('deductions', __name__)
api = Api(deductions_bp)

deduction_parser = reqparse.RequestParser()

deduction_parser.add_argument('deduction_id', type=int, default=True, help="Required deduction identifier")
deduction_parser.add_argument('name', type=str, default=None, help='Deduction name (optional)')
deduction_parser.add_argument('description', type=str, default=None, help='Deduction description (optional)')
deduction_parser.add_argument('amount', type=float, default=None, help='Deduction amount (optional)')
deduction_parser.add_argument('employee_id', type=int, default=None, help='Employee identifier for the deduction')
deduction_parser.add_argument('payroll_id', type=int, default=None, help='Payroll identifier for the deduction (optional) ')

deductions_fields = {
    'deduction_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'amount': fields.Float,
    'employee_id': fields.Integer,
    'payroll_id': fields.Integer,
}

class DeductionResource(Resource):
    @marshal_with(deductions_fields)
    def get(self, deduction_id):
        deduction = Deduction.query.get_or_404(deduction_id)
        return jsonify({
            'deduction_id': deduction.deduction_id,
            'name': deduction.name,
            'description': deduction.description,
            'amount': deduction.amount,
            'employee_id': deduction.employee_id,
            'payroll_id': deduction.payroll_id
        })
    
    @marshal_with(deductions_fields)
    def put(self, deduction_id):
        args = deduction_parser.parse_args()
        deduction = Deduction.query.get_or_404(deduction_id)
        deduction.name = args.get('name')
        deduction.description = args.get('description')
        deduction.amount = args.get('amount')
        deduction.employee_id = args.get('employee_id')
        deduction.payroll_id = args.get('payroll_id')
        db.session.commit()
        return deduction
    
    def delete(self, deduction_id):
        deduction = Deduction.query.get_or_404(deduction_id)
        db.session.delete(deduction)
        db.session.commit()
        return jsonify({'message': 'Deduction deleted successfully'})
    
    @marshal_with(deductions_fields)
    def post(self):
        data = request.get_json()
        new_deduction = Deduction(
            name=data['name'],
            description=data['description'],
            amount=data['amount'],
            employee_id=data['employee_id'],
            payroll_id=data['payroll_id']
        )
        db.session.add(new_deduction)
        db.session.commit()
        return jsonify({
            'deduction_id': new_deduction.deduction_id,
            'name': new_deduction.name,
            'description': new_deduction.description,
            'amount': new_deduction.amount,
            'employee_id': new_deduction.employee_id,
            'payroll_id': new_deduction.payroll_id})
    
    def patch(self, new_deduction):
        data = request.get_json()
        deduction = Deduction.query.get_or_404(new_deduction)
        deduction.name = data.get('name', deduction.name)
        deduction.description = data.get('description', deduction.description)
        deduction.amount = data.get('amount', deduction.amount)
        deduction.employee_id = data.get('employee_id', deduction.employee_id)
        deduction.payroll_id = data.get('payroll_id', deduction.payroll_id)
        db.session.commit()
        return deduction

api.add_resource(DeductionResource, '/deductions/<int:deduction_id>', endpoint='deduction')
deductions_bp.add_url_rule('/deductions', view_func=DeductionResource.as_view('deductions'))