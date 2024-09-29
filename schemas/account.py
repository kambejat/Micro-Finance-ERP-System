from flask_marshmallow import Marshmallow
from models import Account

ma = Marshmallow()

class AccountSchema(ma.Schema):
    class Meta:
        model = Account
        load_instance = True


account_schema = AccountSchema()
account_list_schema = AccountSchema(many=True)