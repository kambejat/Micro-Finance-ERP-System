from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from models import db, Job

jobs_bp = Blueprint('jobs', __name__)

api = Api(jobs_bp)

job_parser = reqparse.RequestParser()

job_parser.add_argument('job_id', type=int, default=True, help="Required job identifier")
job_parser.add_argument('name', type=str, required=True, help="Job name is required")
job_parser.add_argument('title', type=str, required=True, help="Job title is required (default) or default")
job_parser.add_argument('description', type=str, required=True, help="Job description is required")
job_parser.add_argument('salary_range', type=str, required=True, help="Salary range is required")

job_fields = {
    'job_id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'description': fields.String,
    'salary_range': fields.String,
}

class JobResource(Resource):
    @marshal_with(job_fields)
    def get(self, job_id=None):
        if job_id:
            job = Job.query.get_or_404(job_id)
            return job
        jobs = Job.query.all()
        return jsonify(jobs)
    
    @marshal_with(job_fields)
    def post(self):
        data = job_parser.parse_args()
        job = Job(name=data['name'], title=data.get('title', 'Default'), description=data['description'], salary_range=data['salary_range'])
        db.session.add(job)
        db.session.commit()
        return job, 201
    
    @marshal_with(job_fields)
    def put(self, job_id):
        data = job_parser.parse_args()
        job = Job.query.get_or_404(job_id)
        job.name = data['name']
        job.title = data.get('title', 'Default')
        job.description = data['description']
        job.salary_range = data['salary_range']
        db.session.commit()
        return job, 200
    
    def delete(self, job_id):
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        return {'message': 'Job deleted successfully'}, 200
    
    @marshal_with(job_fields)
    def patch(self, job_id):
        data = job_parser.parse_args()
        job = Job.query.get_or_404(job_id)
        if data.get('name'):
            job.name = data['name']
        if data.get('title'):
            job.title = data.get('title', 'Default')
        if data.get('description'):
            job.description = data['description']
        if data.get('salary_range'):
            job.salary_range = data['salary_range']
        db.session.commit()
        return job, 200
    
