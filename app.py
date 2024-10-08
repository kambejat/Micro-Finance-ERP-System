from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS

from models import db
from config import Config

from routes.accounts import accounts_bp
from routes.users import auth_bp
from routes.audit_logs import audit_logs_bp
from routes.bonus import bonuses_bp
from routes.branchs import branches_bp
from routes.categories import categories_bp
from routes.deductions import deductions_bp
from routes.employees import employees_bp
from routes.inventorytransactions import inventory_transactions_bp
from routes.invetories import inventory_bp
from routes.jobs import jobs_bp
from routes.loans import loans_bp
from routes.payments import payments_bp
from routes.payrolls import payroll_bp
from routes.permissions import permissions_bp
from routes.project_teams import project_teams_bp
from routes.projects import projects_bp
from routes.role_permissions import role_permissions_bp
from routes.roles import roles_bp
from routes.tasks import tasks_bp
from routes.team_members import team_members_bp
from routes.teams import teams_bp
from routes.transcations import transactions_bp
from routes.user_roles import user_roles_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    # Enable CORS for all routes
    CORS(app)  # You can restrict this with specific origins if needed

    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    # app route 
    app.register_blueprint(accounts_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(audit_logs_bp, url_prefix='/api')
    app.register_blueprint(bonuses_bp, url_prefix='/api')
    app.register_blueprint(branches_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(deductions_bp, url_prefix='/api')
    app.register_blueprint(employees_bp, url_prefix='/api')
    app.register_blueprint(inventory_transactions_bp, url_prefix='/api')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(jobs_bp, url_prefix='/api')
    app.register_blueprint(loans_bp, url_prefix='/api')
    app.register_blueprint(payments_bp, url_prefix='/api')
    app.register_blueprint(payroll_bp, url_prefix='/api')
    app.register_blueprint(permissions_bp, url_prefix='/api')
    app.register_blueprint(project_teams_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(role_permissions_bp, url_prefix='/api')
    app.register_blueprint(roles_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    app.register_blueprint(team_members_bp, url_prefix='/api')
    app.register_blueprint(teams_bp, url_prefix='/api')
    app.register_blueprint(transactions_bp, url_prefix='/api')
    app.register_blueprint(user_roles_bp, url_prefix='/api')

    @app.route('/')
    def list_routes():
        # List all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'url': rule.rule
                })
        return jsonify(routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
