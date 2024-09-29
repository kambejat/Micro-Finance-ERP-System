from flask_marshmallow import Marshmallow
from models import Deduction

ma = Marshmallow()

class DedutionSchema(ma.Schema):
    class Meta:
        model = Deduction
        load_instance = True


deduction_schema = DedutionSchema()
deduction_list_schema = DedutionSchema(many=True)