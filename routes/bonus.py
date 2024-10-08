from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, Bonus

bonuses_bp = Blueprint('bonuses', __name__)

api = Api(bonuses_bp)

bonus_parser = reqparse.RequestParser()

bonus_parser.add_argument('name', type=str, default=None, help='bonus name (optional)')
bonus_parser.add_argument('description', type=str, default=None, help='bonus description (optional)')
bonus_parser.add_argument('amount', type=float, default=None, help='bonus amount (optional)')
bonus_parser.add_argument('employee_id', type=int, default=None, help='Employee identifier for the bonus')
bonus_parser.add_argument('payroll_id', type=int, default=None, help='Payroll identifier for the bonus (optional) ')

bonuses_fields ={
    'bonus_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'amount': fields.Float,
    'employee_id': fields.Integer,
    'payroll_id': fields.Integer,
}

class BonusResource(Resource):
    @marshal_with(bonuses_fields)
    def get(self, bonus_id):
        bonus = Bonus.query.get_or_404(bonus_id)
        return bonus
    
    @marshal_with(bonuses_fields)
    def put(self, bonus_id):
        data = bonus_parser.parse_args()
        bonus = Bonus.query.get_or_404(bonus_id)
        bonus.name = data.get('name')
        bonus.description = data.get('description')
        bonus.amount = data.get('amount')
        bonus.employee_id = data.get('employee_id')
        bonus.payroll_id = data.get('payroll_id')
        db.session.commit()
        return bonus, 200
    
    def delete(self, bonus_id):
        bonus = Bonus.query.get_or_404(bonus_id)
        db.session.delete(bonus)
        db.session.commit()
        return {'message': 'Bonus deleted successfully'}, 200
    
    @marshal_with(bonuses_fields)
    def post(self):
        data = bonus_parser.parse_args()
        bonus = Bonus(name=data.get('name'), description=data.get('description'), amount=data.get('amount'), employee_id=data.get('employee_id'), payroll_id=data.get('payroll_id'))
        db.session.add(bonus)
        db.session.commit()
        return bonus, 201
    
api.add_resource(BonusResource, '/bonuses/<int:bonus_id>')
bonuses_bp.add_url_rule('/bonuses', view_func=BonusResource.as_view('bonuses'))