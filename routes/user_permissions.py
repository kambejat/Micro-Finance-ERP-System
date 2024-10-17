from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, UserPermission

user_permissions_bp = Blueprint('user_permissions', __name__)

api = Api(user_permissions_bp)

user_permission_parser = reqparse.RequestParser()

user_permission_parser.add_argument('user_id', type=int, default=None, help="Role name")
user_permission_parser.add_argument('permission_id', type=int, default=None, help="ID of the permission")

user_permission_fields = {
    'user_permission_id': fields.Integer,
    'permission_id': fields.Integer,
    'user_id': fields.Integer,
}

class UserPermissionResource(Resource):
    @marshal_with(user_permission_fields)
    def get(self, user_permission_id=None):
        if user_permission_id:
           user_permission = UserPermission.query.get_or_404(user_permission_id)
           return {
                'user_permission_id': user_permission.user_permission_id,
                'permission_id': user_permission.permission_id,
                'user_id': user_permission.user_id,
           }
        user_permissions = UserPermission.query.all()
        return [{
            'user_permission_id': user_permission.user_permission_id,
            'permission_id': user_permission.permission_id,
            'user_id': user_permission.user_id,
        } for user_permission in user_permissions]
    
    def post(self):
        data = request.get_json()
        new_user_permission = UserPermission(
            user_id=data['user_id'],
            permission_id=data['permission_id']
        )
        db.session.add(new_user_permission)
        db.session.commit()
        return new_user_permission, 201
    
    def put(self, user_permission_id):
        data = user_permission_parser.parse_args()
        user_permission = UserPermission.query.get_or_404(user_permission_id)
        user_permission.user_id = data.get('user_id')
        user_permission.permission_id = data.get('permission_id')
        db.session.commit()
        return user_permission
    
    def delete(self, user_permission_id):
        user_permission = UserPermission.query.get_or_404(user_permission_id)
        db.session.delete(user_permission)
        db.session.commit()
        return {'message': 'User permission deleted successfully'}, 200
    
    @marshal_with(user_permission_fields)
    def patch(self, user_permission_id):
        data = user_permission_parser.parse_args()
        user_permission = UserPermission.query.get_or_404(user_permission_id)
        if 'user_id' in data:
            user_permission.user_id = data['user_id']
        if 'permission_id' in data:
            user_permission.permission_id = data['permission_id']
            db.session.commit()
            return user_permission
        return user_permission
    
    def options(self):
        return {'Allow': 'GET, POST, PUT, DELETE, PATCH'}, 200


api.add_resource(UserPermissionResource, '/user_permissions', '/user_permissions/<int:user_permission_id>')
user_permissions_bp.add_url_rule('/user_permissions', view_func=UserPermissionResource.as_view('user_permissions'))