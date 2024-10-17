from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class RoleEnum(Enum):
    ADMIN = "Admin"
    USER = "User"
    GUEST = "Guest"

# Core Modules
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(80), nullable=True)
    isActive = db.Column(db.Boolean, default=False, nullable=True)
    isStaff = db.Column(db.Boolean, default=False, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Permission(db.Model):
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class RolePermission(db.Model):
    role_permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)


class UserPermission(db.Model):
    user_permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)


# Financial Institution Modules
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    opened_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default="Active")


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    transaction_type = db.Column(db.String(50), nullable=False)


class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    term_years = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default="Active")


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.loan_id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))


class Branch(db.Model):
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True) 


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255))
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'))
    hire_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    salary = db.Column(db.Float)
    status = db.Column(db.String(50), default="Active")


class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    salary_range = db.Column(db.String(255))


class AuditLog(db.Model):
    auditlog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    details = db.Column(db.Text)


class InventoryItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class InventoryTransaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.item_id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # e.g., 'IN', 'OUT'
    description = db.Column(db.String(255))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))


class Payroll(db.Model):
    payroll_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    gross_salary = db.Column(db.Float, nullable=False)
    deductions = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., 'Bank Transfer', 'Cash'


class Deduction(db.Model):
    deduction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll.payroll_id'), nullable=False)


class Bonus(db.Model):
    bonus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll.payroll_id'), nullable=False)


# Project Management Modules
class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="Active")
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="Pending")
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    priority = db.Column(db.String(50), default="Medium")


class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))


class TeamMember(db.Model):
    team_member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    role = db.Column(db.String(255))


class ProjectTeam(db.Model):
    project_team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
