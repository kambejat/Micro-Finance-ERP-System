import datetime
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, Project

projects_bp = Blueprint('projects', __name__)
api = Api(projects_bp)

project_parser = reqparse.RequestParser()
project_parser.add_argument('project_id', type=int, default=True, help="Required project identifier")
project_parser.add_argument('name', type=str, default=None, help="Required project name")
project_parser.add_argument('description', type=str, default=None, help="Required project description  (optional)")
project_parser.add_argument('start_date', type=datetime, default=None, help="Required project start date (optional)")
project_parser.add_argument('end_date', type=datetime, default=None, help="Required project end date (optional)")
project_parser.add_argument('status', type=str, default=None, help="Required project status  (optional)")
project_parser.add_argument('manager_id', type=int, default=None, help="Required project manager identifier")

projects_fields = {
    'project_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'start_date': fields.DateTime,
    'end_date': fields.DateTime,
    'status': fields.String,
    'manager_id': fields.Integer
}

class ProjectResource(Resource):
    @marshal_with(projects_fields)
    def get(self):
        project_id = request.args.get('project_id')
        if project_id:
            project = Project.query.get_or_404(project_id)
            return project
        projects = Project.query.all()
        return projects
    
    @marshal_with(projects_fields)
    def post(self):
        data = project_parser.parse_args()
        project = Project(
            name=data['name'],
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            status=data.get('status'),
            manager_id=data['manager_id']
        )
        db.session.add(project)
        db.session.commit()
        return project, 201
    
    @marshal_with(projects_fields)
    def put(self, project_id):
        data = project_parser.parse_args()
        project = Project.query.get_or_404(project_id)
        project.name = data['name']
        project.description = data.get('description')
        project.start_date = data.get('start_date')
        project.end_date = data.get('end_date')
        project.status = data.get('status')
        project.manager_id = data['manager_id']
        db.session.commit()
        return project, 200
    
    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}, 200
    
    @marshal_with(projects_fields)
    def patch(self, project_id):
        data = project_parser.parse_args()
        project = Project.query.get_or_404(project_id)
        if data.get('name'):
            project.name = data['name']
        if data.get('description'):
            project.description = data['description']
        if data.get('start_date'):
            project.start_date = data['start_date']
        if data.get('end_date'):
            project.end_date = data['end_date']
        if data.get('status'):
            project.status = data['status']
        if data.get('manager_id'):
            project.manager_id = data['manager_id']
        db.session.commit()
        return project, 200
  
    
api.add_resource(ProjectResource, '/projects')
projects_bp.add_url_rule('/projects', view_func=ProjectResource.as_view('projects'))