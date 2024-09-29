from flask_marshmallow import Marshmallow
from models import Customer


ma =  Marshmallow()

class CustomerSchema(ma.Schema):
    class Meta:
        model = Customer
        load_instance = True


customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)