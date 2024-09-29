from flask_marshmallow import Marshmallow
from models import TeamMember

ma =  Marshmallow()

class TeamMemberSchema(ma.Schema):
    class Meta:
        model = TeamMember
        load_instance = True


team_member_schema = TeamMemberSchema()
team_member_schemas = TeamMemberSchema(many=True)