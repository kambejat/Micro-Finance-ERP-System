from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, Category

categories_bp = Blueprint('categories', __name__)

api = Api(categories_bp)

category_parser = reqparse.RequestParser()

category_parser.add_argument('name', type=str, required=True, help="Category name is required")
category_parser.add_argument('description', type=str, required=True, help="Description of the category")

categories_fields = {
    'category_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}


class CategoryResource(Resource):
    @marshal_with(categories_fields)
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get_or_404(category_id)
            return category
        else:
            categories = Category.query.all()
            return categories
        
    @marshal_with(categories_fields)
    def post(self):
        data = category_parser.parse_args()
        category = Category(name=data['name'], description=data['description'])
        db.session.add(category)
        db.session.commit()
        return category, 201
    
    @marshal_with(categories_fields)
    def put(self, category_id):
        data = category_parser.parse_args()
        category = Category.query.get_or_404(category_id)
        category.name = data['name']
        category.description = data['description']
        db.session.commit()
        return category, 200
    
    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}, 200
    

api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
categories_bp.add_url_rule('category', view_func=CategoryResource.as_view('category'))