from flask_marshmallow import Marshmallow
from models import Payment

ma = Marshmallow()

class PaymentSchema(ma.Schema):
    class Meta:
        model = Payment
        load_instance = True


payment_schema = PaymentSchema()
payment_list_schema = PaymentSchema(many=True)