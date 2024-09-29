from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from models import db, Team

teams_bp = Blueprint('teams', __name__) 
api = Api(teams_bp)

team_parser = reqparse.RequestParser()

team_parser.add_argument('team_id', type=int, default=True, help="Required team identifier")
team_parser.add_argument('name', type=str, default=None, help="Team name to be used for team creation")
team_parser.add_argument('description', type=str, default=None, help="Team description to be used for team creation")

team_fields = {
    'team_id': fields.Integer,
    'name': fields.String,
    'description': fields.String
    }

class TeamResource(Resource):
    @marshal_with(team_fields)
    def get(self, team_id=None):
        if team_id:
            team = Team.query.get_or_404(team_id)
            return team
        else:
            teams = Team.query.all()
            return {'teams': [marshal(team, team_fields) for team in teams]}
        
    @marshal_with(team_fields)
    def post(self):
        data = team_parser.parse_args()
        new_team = Team(name=data['name'], description=data['description'])
        db.session.add(new_team)
        db.session.commit()
        return new_team, 201
    
    @marshal_with(team_fields)
    def put(self, team_id):
        data = team_parser.parse_args()
        team = Team.query.get_or_404(team_id)
        team.name = data['name']
        team.description = data['description']
        db.session.commit()
        return team, 200
    
    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return {'message': 'Team deleted successfully'}, 200
    
    @marshal_with(team_fields)
    def patch(self, team_id):
        data = team_parser.parse_args()
        team = Team.query.get_or_404(team_id)
        for key, value in data.items():
            if value is not None:
                setattr(team, key, value)
        db.session.commit()
        return team, 200
    
api.add_resource(TeamResource, '/teams', '/teams/<int:team_id>')
teams_bp.add_url_rule('/teams', view_func=TeamResource.as_view('teams'))