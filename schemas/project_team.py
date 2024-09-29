from flask_marshmallow import Marshmallow
from models import ProjectTeam

ma = Marshmallow()

class ProjectTeamSchema(ma.Schema):
    class Meta:
        model = ProjectTeam
        load_instance = True


project_team_schema = ProjectTeamSchema()
project_team_schemas = ProjectTeamSchema(many=True)