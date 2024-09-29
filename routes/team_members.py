from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, TeamMember

team_members_bp = Blueprint('team_members', __name__)
api = Api(team_members_bp)

team_member_parser = reqparse.RequestParser()

team_member_parser.add_argument('team_member_id', type=int, default=True, help="Required team member identifier")
team_member_parser.add_argument("team_id", type=int, default=None, help="Team identifier for the team")
team_member_parser.add_argument("user_id", type=int, default=None, help="User identifier for the team")
team_member_parser.add_argument("role", type=str, default=None, help="Role for the team member")

team_member_fields = {
    "team_member_id": fields.Integer,
    "team_id": fields.Integer,
    "user_id": fields.Integer,
    "role": fields.String
}

class TeamMemberResource(Resource):
    @marshal_with(team_member_fields)
    def get(self, team_member_id=None):
        if team_member_id:
            team_member = TeamMember.query.get_or_404(team_member_id)
            return team_member
        else:
            team_members = TeamMember.query.all()
            return team_members
        
    @marshal_with(team_member_fields)
    def post(self):
        data = team_member_parser.parse_args()
        team_member = TeamMember(team_id=data["team_id"], user_id=data["user_id"], role=data["role"])
        db.session.add(team_member)
        db.session.commit()
        return team_member, 201
    
    @marshal_with(team_member_fields)
    def put(self, team_member_id):
        data = team_member_parser.parse_args()
        team_member = TeamMember.query.get_or_404(team_member_id)
        team_member.team_id = data.get("team_id")
        team_member.user_id = data.get("user_id")
        team_member.role = data.get("role")
        db.session.commit()
        return team_member, 200
    
    def delete(self, team_member_id):
        team_member = TeamMember.query.get_or_404(team_member_id)
        db.session.delete(team_member)
        db.session.commit()
        return {"message": "Team member deleted successfully"}, 200
    
api.add_resource(TeamMemberResource, "/team_members", "/team_members/<int:team_member_id>")
team_members_bp.add_url_rule("/team_members", view_func=TeamMemberResource.as_view("team_members"))