from flask_marshmallow import Marshmallow
from models import Payroll

ma = Marshmallow()

class PayrollSchema(ma.Schema):
    class Meta:
        model = Payroll
        load_instance = True


payroll_schema = PayrollSchema()
payroll_schemas = PayrollSchema(many=True)