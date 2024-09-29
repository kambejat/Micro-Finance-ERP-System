from flask_marshmallow import Marshmallow
from models import RolePermission

ma = Marshmallow()

class RolePermissionSchema(ma.Schema):
    class Meta:
        model = RolePermission
        load_instance = True


role_permission_schema = RolePermissionSchema()
role_permission_schemas = RolePermissionSchema(many=True)