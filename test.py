import logging
from sqlalchemy.exc import IntegrityError
from models import db, Permission

def add_permissions(db):
    permissions = [
        {"name": "view_users", "description": "Permission to view users"},
        {"name": "add_users", "description": "Permission to add users"},
        {"name": "edit_users", "description": "Permission to edit users"},
        {"name": "delete_users", "description": "Permission to delete users"},
        {"name": "view_audit_logs", "description": "Permission to view audit logs"},
        {"name": "manage_roles", "description": "Permission to manage roles and permissions"},
    ]
    
    for perm in permissions:
        permission = Permission(name=perm['name'], description=perm['description'])
        db.session.add(permission)
    
    try:
        db.session.commit()
        return True, "Permissions added successfully."
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error adding permissions: {e}")  # Log the error
        return False, "Some permissions already exist or there was an error inserting them."
