from flask_marshmallow import Marshmallow
from models import UserRole

ma = Marshmallow()

class UserRoleSchema(ma.Schema):
    class Meta:
        model = UserRole
        load_instance = True

user_role_schema = UserRoleSchema()
user_role_schemas = UserRoleSchema(many=True)