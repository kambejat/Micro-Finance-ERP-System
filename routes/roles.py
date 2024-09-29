from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from models import db, Role

roles_bp = Blueprint('roles', __name__)

api = Api(roles_bp)

role_parser = reqparse.RequestParser()

role_parser.add_argument('role_id', type=int, default=True, help="Required role identifier")
role_parser.add_argument('name', type=str, default=None, help="Role name to be used for role creation")
role_parser.add_argument('description', type=str, default=None, help="Role description to be used for role creation")

role_fields = {
    'role_id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

class RoleResource(Resource):
    @marshal_with(role_fields)
    def get(self, role_id=None):
        if role_id:
            role = Role.query.get_or_404(role_id)
            return role
        else:
            roles = Role.query.all()
            return {'roles': [marshal(role, role_fields) for role in roles]}
    
    @marshal_with(role_fields)
    def post(self):
        data = role_parser.parse_args()
        new_role = Role(name=data['name'], description=data['description'])
        db.session.add(new_role)
        db.session.commit()
        return new_role, 201
    
    @marshal_with(role_fields)
    def put(self, role_id):
        data = role_parser.parse_args()
        role = Role.query.get_or_404(role_id)
        role.name = data['name']
        role.description = data['description']
        db.session.commit()
        return role, 200
    
    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        return {'message': 'Role deleted successfully'}, 200
    
    @marshal_with(role_fields)
    def patch(self, role_id):
        data = role_parser.parse_args()
        role = Role.query.get_or_404(role_id)
        if data['name']:
            role.name = data['name']
        if data['description']:
            role.description = data['description']
        db.session.commit()
        return role, 200

api.add_resource(RoleResource, '/roles/<int:role_id>')
roles_bp.add_url_rule('/roles', view_func=RoleResource.as_view('roles'))