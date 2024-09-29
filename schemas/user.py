from flask_marshmallow import Marshmallow
from models import User

ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
user_schemas = UserSchema(many=True)