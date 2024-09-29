from flask_marshmallow import Marshmallow
from models import Task

ma = Marshmallow()

class TaskSchema(ma.Schema):
    class Meta:
        model = Task
        load_instance = True


task_schema = TaskSchema()
task_schemas = TaskSchema(many=True)