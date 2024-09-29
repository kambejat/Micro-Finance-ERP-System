from flask_marshmallow import Marshmallow
from models import Bonus

ma = Marshmallow()

class BonusSchema(ma.Schema):
    class Meta:
        model = Bonus
        load_instance = True


bonus_schema = BonusSchema()
bonus_schema_list = BonusSchema(many=True)
