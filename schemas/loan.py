from flask_marshmallow import Marshmallow
from models import Loan

ma = Marshmallow()

class LoanSchema(ma.Schema):
    class Meta:
        model = Loan
        load_instance = True


loan_schema = LoanSchema()
loan_list_schema= LoanSchema(many=True)