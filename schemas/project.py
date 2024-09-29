from flask_marshmallow import Marshmallow
from models import Project

ma = Marshmallow()

class ProjectSchema(ma.Schema):
    class Meta:
        model = Project
        load_instance = True


project_schema = ProjectSchema()
project_schemas = ProjectSchema(many=True)