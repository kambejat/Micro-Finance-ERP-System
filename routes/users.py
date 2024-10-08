from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash
from models import db, User, Role

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

# user_parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, default=None, help='Username is required')
user_parser.add_argument('password', type=str, default=None, help='Password is required')
user_parser.add_argument('email', type=str, default=None, help='Email address is required')
user_parser.add_argument('fullname', type=str, default=None, help='Enter full name')
user_parser.add_argument('role_id', type=str, default=None, help='Role identifier is required')

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "role_id": user.role_id
            }
        users = User.query.all()
        return [{
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "fullname": user.fullname,
            "role_id": user.role_id
        } for user in users]

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            fullname=data['fullname'],
            profile_image=data.get('profile_image'),
            role_id=data['role_id']
        )
        new_user.set_password(data['password_hash'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully", "user_id": new_user.user_id}, 201

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data['username']
        user.email = data['email']
        user.fullname = data['fullname']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return {"message": "User updated successfully"}, 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    

class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            role = Role.query.get(user.role_id)
            
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "fullname": user.fullname,
                    "role": role.name
                }
            }, 200
        return {"message": "Invalid credentials"}, 401
    

# Register resources
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserLoginResource, '/users/login')
