import datetime
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from models import db, Task

tasks_bp = Blueprint('tasks', __name__)
api = Api(tasks_bp)

task_parser = reqparse.RequestParser()

task_parser.add_argument('task_id', type=int, default=True, help="Required task identifier")
task_parser.add_argument('project_id', type=int, default=True, help="Required project identifier")
task_parser.add_argument('name', type=str, default=None, help="Required task name")
task_parser.add_argument('description', type=str, default=None, help="Required task description")
task_parser.add_argument('start_date', type=datetime.datetime, default=None, help="Required task start date")
task_parser.add_argument('due_date', type=datetime.datetime, default=None, help="Required task due date")
task_parser.add_argument('status', type=str, default=None, help="Required task status")
task_parser.add_argument('assigned_to', type=int, default=None, help="Required task assigned to task")
task_parser.add_argument('priority', type=str, default=None, help="Required task priority (default priority is medium)")

tasks_fields = {
    'task_id': fields.Integer,
    'project_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'start_date': fields.DateTime(dt_format='iso8601'),
    'due_date': fields.DateTime(dt_format='iso8601'),
    'status': fields.String,
    'assigned_to': fields.Integer,
    'priority': fields.String
}

class TaskResource(Resource):
    @marshal_with(tasks_fields)
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task
    
    @marshal_with(tasks_fields)
    def put(self, task_id):
        data = task_parser.parse_args()
        task = Task.query.get_or_404(task_id)
        task.name = data.get('name')
        task.description = data.get('description')
        task.start_date = data.get('start_date')
        task.due_date = data.get('due_date')
        task.status = data.get('status')
        task.assigned_to = data.get('assigned_to')
        task.priority = data.get('priority', 'medium')
        db.session.commit()
        return task, 200
    
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 200
    
    @marshal_with(tasks_fields)
    def post(self):
        data = task_parser.parse_args()
        task = Task(
            project_id=data.get('project_id'),
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            due_date=data.get('due_date'),
            status=data.get('status'),
            assigned_to=data.get('assigned_to'),
            priority=data.get('priority', 'medium')
        )
        db.session.add(task)
        db.session.commit()
        return task, 201
    
    @marshal_with(tasks_fields)
    def patch(self, task_id):
        data = task_parser.parse_args()
        task = Task.query.get_or_404(task_id)
        if data.get('name'):
            task.name = data.get('name')
        if data.get('description'):
            task.description = data.get('description')
        if data.get('start_date'):
            task.start_date = data.get('start_date')
        if data.get('due_date'):
            task.due_date = data.get('due_date')
        if data.get('status'):
            task.status = data.get('status')
        if data.get('assigned_to'):
            task.assigned_to = data.get('assigned_to')
        if data.get('priority'):
            task.priority = data.get('priority', 'medium')
        db.session.commit()
        return task, 200
    

api.add_resource(TaskResource, '/tasks/<int:task_id>')
tasks_bp.add_url_rule('/tasks', view_func=TaskResource.as_view('tasks'))