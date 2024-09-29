from flask_marshmallow import Marshmallow
from models import Job

ma = Marshmallow()

class JobSchema(ma.Schema):
    class Meta:
        model = Job
        load_instance = True


job_schema = JobSchema()
job_list_schema = JobSchema(many=True)