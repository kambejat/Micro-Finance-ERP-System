from flask_marshmallow import Marshmallow
from models import AuditLog

ma =  Marshmallow()

class AuditLogSchema(ma.Schema):
    class Meta:
        model = AuditLog
        load_instance = True


audit_log_schema = AuditLogSchema()
audit_log_schemas = AuditLogSchema(many=True)