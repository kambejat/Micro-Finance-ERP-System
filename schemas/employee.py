from flask_marshmallow import Marshmallow
from models import Employee

ma =  Marshmallow()

class EmployeeSchema(ma.Schema):
    class Meta:
        model= Employee
        load_instance =  True


employee_schema = EmployeeSchema()
employee_list_schema = EmployeeSchema(many=True)