from flask_marshmallow import Marshmallow
from models import Role

ma = Marshmallow()

class RoleSchema(ma.Schema):
    class Meta:
        model = Role
        load_instance = True


role_schema = RoleSchema()
role_schemas = RoleSchema(many=True)