from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, marshal, marshal_with, fields
from models import db, ProjectTeam

project_teams_bp = Blueprint('project_teams', __name__)

api = Api(project_teams_bp)

project_team_parser = reqparse.RequestParser()

project_team_parser.add_argument('project_team_id', type=int, default=True, help="Required project team identifier")
project_team_parser.add_argument('project_id', type=int, default=None, help="Required project identifier (optional)")
project_team_parser.add_argument('team_id', type=int, default=None, help="Required team identifier (optional) or team name (optional)")

project_team_fields = {
    'project_team_id': fields.Integer,
    'project_id': fields.Integer,
    'team_id': fields.Integer,
}

class ProjectTeamResource(Resource):
    def get(self, project_team_id=None):
        if project_team_id:
            project_team = ProjectTeam.query.get_or_404(project_team_id)
            return jsonify({
                'project_team_id': project_team.project_team_id,
                'project_id': project_team.project_id,
                'team_id': project_team.team_id,
            })
    
    @marshal_with(project_team_fields)
    def put(self, project_team_id):
        data = project_team_parser.parse_args()
        project_team = ProjectTeam.query.get_or_404(project_team_id)
        project_team.project_id = data.get('project_id')
        project_team.team_id = data.get('team_id')
        db.session.commit()
        return project_team
    
    def delete(self, project_team_id):
        project_team = ProjectTeam.query.get_or_404(project_team_id)
        db.session.delete(project_team)
        db.session.commit()
        return jsonify({'message': 'Project team deleted'})
    
    @marshal_with(project_team_fields)
    def post(self):
        data = project_team_parser.parse_args()
        project_team = ProjectTeam(project_id=data.get('project_id'), team_id=data.get('team_id'))
        db.session.add(project_team)
        db.session.commit()
        return project_team, 201
    
    def patch(self, project_id):
        project_teams = ProjectTeam.query.filter_by(project_id=project_id).all()
        for project_team in project_teams:
            project_team.project_id = None
            project_team.team_id = None
        db.session.commit()
        return jsonify({'message': 'All project teams for project deleted'})


api.add_resource(ProjectTeamResource, '/project_teams', '/project_teams/<int:project_team_id>')
project_teams_bp.add_url_rule('/project_teams', view_func=ProjectTeamResource.as_view('project_teams'))
