from flask_marshmallow import Marshmallow
from models import Category

ma =  Marshmallow()

class CategorySchema(ma.Schema):
    class Meta:
        model = Category
        load_instance = True

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)