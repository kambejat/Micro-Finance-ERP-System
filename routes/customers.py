import datetime
from flask import Blueprint
from flask_restful  import Api, Resource, reqparse, fields, marshal_with
from models import db, Customer

customers_bp = Blueprint('customers', __name__)

api = Api(customers_bp)

customer_parser = reqparse.RequestParser()

customer_parser.add_argument('name', type=str, default=None, help="Name of the customer to create")
customer_parser.add_argument('address', type=str, default=None, help="Address of the customer to create")
customer_parser.add_argument('email', type=str, default=None, help="Email address of the customer to create")
customer_parser.add_argument('contact_info', type=str, default=None, help="Contact information for the customer to create")
customer_parser.add_argument('created_at', type=datetime.datetime, default=None, help="Date and time when the customer was created to create")

customer_fields = {
    'customer_id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'email': fields.String,
    'contact_info': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
}


class CustomerResource(Resource):
    @marshal_with(customer_fields)
    def get(self, customer_id=None):
        if customer_id:
            customer = Customer.query.get_or_404(customer_id)
            return customer
        customers = Customer.query.all()
        return customers
    
    @marshal_with(customer_fields)
    def post(self):
        data = customer_parser.parse_args()
        new_customer = Customer(
            name=data['name'],
            address=data['address'],
            email=data['email'],
            contact_info=data['contact_info'],
            created_at=datetime.datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()
        return new_customer, 201
    
    @marshal_with(customer_fields)
    def put(self, customer_id):
        data = customer_parser.parse_args()
        customer = Customer.query.get_or_404(customer_id)
        customer.name = data['name']
        customer.address = data['address']
        customer.email = data['email']
        customer.contact_info = data['contact_info']
        db.session.commit()
        return customer, 200
    
    def delete(self, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted successfully'}, 200
    
    def patch(self, customer):
        data = customer_parser.parse_args()
        customer.name = data.get('name', customer.name)
        customer.address = data.get('address', customer.address)
        customer.email = data.get('email', customer.email)
        customer.contact_info = data.get('contact_info', customer.contact_info)
        db.session.commit()
        return customer, 200
    

api.add_resource(CustomerResource, '/customers', '/customers/<int:customer_id>')
customers_bp.add_url_rule('/customers', view_func=CustomerResource.as_view('customers'))