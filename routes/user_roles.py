from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, marshal_with, fields
from models import db, UserRole

user_roles_bp = Blueprint('user_roles', __name__)

api = Api(user_roles_bp)

user_roles_parser = reqparse.RequestParser()

user_roles_parser.add_argument('user_role_id', type=int, default=True, help="Required user role identifier")
user_roles_parser.add_argument("role_id", type=int, default=None, help="Required role identifier")
user_roles_parser.add_argument("user_id", type=int, default=None, help="Required user identifier")

user_role_fields = {
    'user_role_id': fields.Integer,
    'role_id': fields.Integer,
    'user_id': fields.Integer,
}

class UserRoleResource(Resource):
    def get(self, user_role_id=None):
        if user_role_id:
            user_role = UserRole.query.get_or_404(user_role_id)
            return marshal(user_role, user_role_fields)
        else:
            user_roles = UserRole.query.all()
            return marshal(user_roles, [user_role_fields])
    
    def post(self):
        data = user_roles_parser.parse_args()
        new_user_role = UserRole(
            role_id=data['role_id'],
            user_id=data['user_id']
        )
        db.session.add(new_user_role)
        db.session.commit()
        return marshal(new_user_role, user_role_fields), 201
    
    def put(self, user_role_id):
        data = user_roles_parser.parse_args()
        user_role = UserRole.query.get_or_404(user_role_id)
        user_role.role_id = data['role_id']
        user_role.user_id = data['user_id']
        db.session.commit()
        return marshal(user_role, user_role_fields)
    
    def delete(self, user_role_id):
        user_role = UserRole.query.get_or_404(user_role_id)
        db.session.delete(user_role)
        db.session.commit()
        return {'message': 'User role deleted successfully'}, 200
    
    def patch(self, user_role_id):
        data = user_roles_parser.parse_args()
        user_role = UserRole.query.get_or_404(user_role_id)
        if 'role_id' in data:
            user_role.role_id = data['role_id']
            db.session.commit()
            return marshal(user_role, user_role_fields)
        if 'user_id' in data:
            user_role.user_id = data['user_id']
            db.session.commit()
            return marshal(user_role, user_role_fields)
        return {'message': 'No data provided for update'}, 400

api.add_resource(UserRoleResource, '/user_roles', '/user_roles/<int:user_role_id>')

user_roles_bp.add_url_rule('/user_roles', view_func=UserRoleResource.as_view('user_roles'))