from flask_marshmallow import Marshmallow
from models import Team

ma =  Marshmallow()

class TeamSchema(ma.Schema):
    class Meta:
        model = Team
        load_instance = True


team_schema = TeamSchema()
team_schemas = TeamSchema(many=True)