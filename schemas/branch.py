from flask_marshmallow import Marshmallow
from models import Branch

ma = Marshmallow()

class BranchSchema(ma.Schema):
    class Meta:
        model = Branch
        load_instance = True


branch_schema = BranchSchema()
branch_list_schema = BranchSchema(many=True)
