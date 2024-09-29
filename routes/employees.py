import datetime
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, Employee


employees_bp = Blueprint('employees', __name__)
api = Api(employees_bp)

employee_parser = reqparse.RequestParser()

employee_parser.add_argument('employee_id', type=int, default=True, help="Required employee identifier")
employee_parser.add_argument('name', type=str, default=None, help="Name of employee to create or update in database")
employee_parser.add_argument('contact_info', type=str, default=None, help="Contact information for employee to create or update in database")
employee_parser.add_argument('job_id', type=int, default=None, help="Job ID to create or update")
employee_parser.add_argument('branch_id', type=int, default=None, help="Branch ID to create or update ")
employee_parser.add_argument('hire_date', type=datetime.datetime, default=None, help="Date to be hired in database")
employee_parser.add_argument('salary', type=float, default=None, help="Amount to allocate for employee to create or update ")
employee_parser.add_argument('status', type=str, default=None, help="Status of employee to create or update in database")

employees_fields = {
    'employee_id': fields.Integer,
    'name': fields.String,
    'contact_info': fields.String,
    'job_id': fields.Integer,
    'branch_id': fields.Integer,
    'hire_date': fields.DateTime,
    'salary': fields.Float,
   'status': fields.String
}

class EmployeeResource(Resource):
    @marshal_with(employees_fields)
    def get(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        return employee
    
    @marshal_with(employees_fields)
    def put(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        data = employee_parser.parse_args()
        for key, value in data.items():
            if value is not None:
                setattr(employee, key, value)
        db.session.commit()
        return employee
    
    @marshal_with(employees_fields)
    def delete(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Employee deleted successfully'}, 200
    
    def post(self):
        data = employee_parser.parse_args()
        employee = Employee(name=data['name'], contact_info=data['contact_info'], job_id=data['job_id'], branch_id=data['branch_id'], hire_date=data['hire_date'], salary=data['salary'], status=data['status'])
        db.session.add(employee)
        db.session.commit()
        return employee, 201
    
    def patch(self, employee_id, employee):
        data = employee_parser.parse_args()
        employee = Employee.query.get_or_404(employee_id)
        for key, value in data.items():
            if value is not None:
                setattr(employee, key, value)
        db.session.commit()
        return employee

api.add_resource(EmployeeResource, '/employees/<int:employee_id>')
employees_bp.add_url_rule('/employees', view_func=EmployeeResource.as_view('employees'))
    
