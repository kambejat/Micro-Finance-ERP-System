from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, Permission

permissions_bp = Blueprint('permissions', __name__)

api = Api(permissions_bp)

permission_parser = reqparse.RequestParser()

permission_parser.add_argument('permission_id', type=int, default=True, help="Required permission identifier")
permission_parser.add_argument('name', type=str, default=None, help="Name of the permission  to be granted to the user")
permission_parser.add_argument('description', type=str, default=None, help="Description of the permission to be granted to the user")

permission_fields = {
    'permission_id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

class PermissionResource(Resource):
    @marshal_with(permission_fields)
    def get(self, permission_id=None):
        if permission_id:
            permission = Permission.query.get_or_404(permission_id)
            return permission
        else:
            return Permission.query.all()
    
    def post(self):
        data = permission_parser.parse_args()
        permission = Permission(name=data.get('name'), description=data.get('description'))
        db.session.add(permission)
        db.session.commit()
        return {'message': 'Permission created successfully', 'permission_id': permission.permission_id}, 201

    @marshal_with(permission_fields)
    def put(self, permission_id):
        data = permission_parser.parse_args()
        permission = Permission.query.get_or_404(permission_id)
        permission.name = data.get('name')
        permission.description = data.get('description')
        db.session.commit()
        return permission
    
    def delete(self, permission_id):
        permission = Permission.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return {'message': 'Permission deleted successfully'}, 200

    @marshal_with(permission_fields)
    def patch(self, permission_id):
        data = permission_parser.parse_args()
        permission = Permission.query.get_or_404(permission_id)
        if 'name' in data:
            permission.name = data['name']
        if 'description' in data:
            permission.description = data['description']
        db.session.commit()
        return permission
    

api.add_resource(PermissionResource, '/permissions', '/permissions/<int:permission_id>')
permissions_bp.add_url_rule('/permissions', view_func=PermissionResource.as_view('permissions'))