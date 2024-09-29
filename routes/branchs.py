from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from models import db, Branch
from sqlalchemy.orm.exc import NoResultFound

branches_bp = Blueprint('branches', __name__)

api = Api(branches_bp)

branch_parser = reqparse.RequestParser()

branch_parser.add_argument('branch_id', type=int, default=True, help="Required branch identifier")
branch_parser.add_argument('name', type=str, required=True, help="Branch name is required")
branch_parser.add_argument('location', type=str, required=True, help="Branch location is required")
branch_parser.add_argument('manager_id', type=int, required=True, help="Manager identifier is required")

branches_fields = {
    'branch_id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'manager_id': fields.Integer
}

class BranchResource(Resource):
    @marshal_with(branches_fields)
    def get(self, branch_id=None):
        if branch_id:
            branch = Branch.query.get_or_404(branch_id)
            return branch
        branches = Branch.query.all()
        return branches
    
    @marshal_with(branches_fields)
    def post(self):
        data = branch_parser.parse_args()
        branch = Branch(name=data['name'], location=data['location'], manager_id=data['manager_id'])
        db.session.add(branch)
        db.session.commit()
        return branch, 201
    
    @marshal_with(branches_fields)
    def put(self, branch_id):
        data = branch_parser.parse_args()
        branch = Branch.query.get_or_404(branch_id)
        branch.name = data.get('name')
        branch.location = data.get('location')
        branch.manager_id = data.get('manager_id')
        db.session.commit()
        return branch, 200
    
    def delete(self, branch_id):
        branch = Branch.query.get_or_404(branch_id)
        db.session.delete(branch)
        db.session.commit()
        return {'message': 'Branch deleted successfully'}, 200
    
    def patch(self, branch_id):
        # Parse the incoming data
        data = branch_parser.parse_args()

        # Fetch the branch from the database based on branch_id
        try:
            branch = Branch.query.filter_by(id=branch_id).one()
        except NoResultFound:
            return {'message': f'Branch with ID {branch_id} not found.'}, 404

        # Update only the fields that are present in the parsed data
        for key, value in data.items():
            if value is not None:
                setattr(branch, key, value)
        
        # Commit the changes to the database
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback in case of any error
            return {'message': f'Failed to update branch: {str(e)}'}, 500
        
        return jsonify(branch), 200
    