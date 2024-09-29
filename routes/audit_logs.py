from flask import Blueprint, jsonify, request
from models import db, AuditLog
from flask_restful import Api, Resource, reqparse

audit_logs_bp = Blueprint('audit_logs', __name__)

api = Api(audit_logs_bp)

audit_log_parser = reqparse.RequestParser()
audit_log_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
audit_log_parser.add_argument('action', type=str, required=True, help='Action is required')
audit_log_parser.add_argument('date', type=str, required=True, help='Date is required')
audit_log_parser.add_argument('details', type=str)


class AuditLogResource(Resource):
    def get(self, log_id=None):
        if log_id:
            log = AuditLog.query.get(log_id)
            if log:
                return jsonify({
                    'auditlog_id': log.auditlog_id,
                    'user_id': log.user_id,
                    'action': log.action,
                    'date': log.date,
                    'details': log.details
                })
            return {'message': 'Audit log not found'}, 404
        else:
            logs = AuditLog.query.all()
            return jsonify([{
                'auditlog_id': log.auditlog_id,
                'user_id': log.user_id,
                'action': log.action,
                'date': log.date,
                'details': log.details
            } for log in logs])

    def post(self):
        data = request.get_json()
        new_log = AuditLog(
            user_id=data['user_id'],
            action=data['action'],
            details=data.get('details', '')
        )
        db.session.add(new_log)
        db.session.commit()
        return {'message': 'Audit log created', 'auditlog_id': new_log.auditlog_id}, 201

    def put(self, log_id):
        data = request.get_json()
        log = AuditLog.query.get(log_id)
        if not log:
            return {'message': 'Audit log not found'}, 404
        log.user_id = data['user_id']
        log.action = data['action']
        log.details = data.get('details', log.details)
        db.session.commit()
        return {'message': 'Audit log updated'}, 200

    def delete(self, log_id):
        log = AuditLog.query.get(log_id)
        if not log:
            return {'message': 'Audit log not found'}, 404
        db.session.delete(log)
        db.session.commit()
        return {'message': 'Audit log deleted'}, 200

# Add API endpoint
api.add_resource(AuditLogResource, '/auditlogs', '/auditlogs/<int:log_id>')