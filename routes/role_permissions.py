from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, RolePermission

role_permissions_bp = Blueprint('role_permissions', __name__)

api = Api(role_permissions_bp)

role_permission_parser = reqparse.RequestParser()

role_permission_parser.add_argument('role_permission_id', type=int, default=True, help="Required role permission identifier")
role_permission_parser.add_argument('role_id', type=int, default=None, help="Role identifier")
role_permission_parser.add_argument('permission_id', type=int, default=None, help="Permission identifier for the role permission")

role_permission_fields = {
    'role_permission_id': fields.Integer,
    'role_id': fields.Integer,
    'permission_id': fields.Integer
}

class RolePermissionResource(Resource):
    @marshal_with(role_permission_fields)
    def get(self, role_permission_id=None):
        if role_permission_id:
            role_permission = RolePermission.query.get_or_404(role_permission_id)
            return role_permission
        else:
            return jsonify({'error': 'Role permission not found'}), 404
    
    @marshal_with(role_permission_fields)
    def put(self, role_permission_id):
        data = role_permission_parser.parse_args()
        role_permission = RolePermission.query.get_or_404(role_permission_id)
        role_permission.role_id = data.get('role_id')
        role_permission.permission_id = data.get('permission_id')
        db.session.commit()
        return role_permission, 200
    
    def delete(self, role_permission_id):
        role_permission = RolePermission.query.get_or_404(role_permission_id)
        db.session.delete(role_permission)
        db.session.commit()
        return {'message': 'Role permission deleted successfully'}, 200
    
    @marshal_with(role_permission_fields)
    def post(self):
        data = role_permission_parser.parse_args()
        role_permission = RolePermission(role_id=data.get('role_id'), permission_id=data.get('permission_id'))
        db.session.add(role_permission)
        db.session.commit()
        return role_permission, 201
    
    def patch(self, role_permission):
        data = role_permission_parser.parse_args()
        role_permission = RolePermission.query.get_or_404(role_permission.role_permission_id)
        if data.get('role_id'):
            role_permission.role_id = data.get('role_id')
        if data.get('permission_id'):
            role_permission.permission_id = data.get('permission_id')
        db.session.commit()
        return role_permission, 200
    
    def options(self, role_permission_id=None):
        return {'allow': ['GET', 'PUT', 'DELETE', 'POST', 'PATCH', 'OPTIONS']}

api.add_resource(RolePermissionResource, '/role_permissions', '/role_permissions/<int:role_permission_id>')
role_permissions_bp.add_url_rule('/role_permissions', view_func=RolePermissionResource.as_view('role_permissions'))