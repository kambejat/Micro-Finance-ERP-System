import os
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, User

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

# user_parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, default=None, help='username is required')
user_parser.add_argument('password', type=str, default=None, help='password is required')
user_parser.add_argument('email', type=str, default=None, help='Email address is required')
user_parser.add_argument('fullname', type=str, default=None, help='Enter full name')
user_parser.add_argument('role_id', type=str, default=None, help='Role identifier is required')

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return jsonify({
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "role_id": user.role_id
            })
        users = User.query.all()
        return jsonify([{
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "fullname": user.fullname,
            "role_id": user.role_id
        } for user in users])

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            fullname=data['fullname'],
            role_id=data['role_id']
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user_id": new_user.user_id})

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data['username']
        user.email = data['email']
        user.fullname = data['fullname']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "User updated successfully"})

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    

class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "fullname": user.fullname,
                    "role_id": user.role_id
                }
            })
        return jsonify({"message": "Invalid credentials"}), 401
    

api.add_resource(UserResource, '/users')
api.add_resource(UserLoginResource, '/users/login')