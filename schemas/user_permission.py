from flask_marshmallow import Marshmallow
from models import UserPermission


ma = Marshmallow()


class UserPermission(ma.Schema):
    class Meta:
        model = UserPermission
        load_instance = True


user_permission_schema = UserPermission()
user_permission_list_schema = UserPermission(many=True)